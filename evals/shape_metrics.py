#!/usr/bin/env python3
"""Measure the shape of replies without an LLM judge.

Reads a responses file in the blind_eval.py format (a JSON array of records with
case_id, repetition, condition and response) and prints aggregates per condition.
The same input always gives the same numbers.

Per reply:

- words: word count of the whole reply;
- to_point: words the reader passes before the point, located by the case's
  pattern in answer-keys.json. Cases without a key are skipped; a reply where
  the pattern is not found counts its whole length and is reported as missed;
- point_first: the pattern matches inside the first sentence (headings skipped);
- longest_block: words in the longest unbroken block. A prose paragraph is one
  block; each list item or table row is its own block; headings are excluded;
- longest_sentence: words in the longest sentence;
- headings: number of Markdown headings;
- opener: the first sentence opens with a ceremonial phrase ("Хороший вопрос",
  "Sure");
- wrapper: the first paragraph presents a deliverable ("Вот вариант", "Here's");
- closer: the last paragraph offers more help or signs off ("Если хотите",
  "Let me know");
- questions: sentences that end with a question mark. For a reply with a
  question, question_last says the reply ends with one, and after_question
  counts the words that follow the last one.

For a case that asks for a ready text (a letter, a message, a commit message),
the key file's deliverables entry gives patterns for the text's first and last
words. Fence lines are ignored, so a text inside a code block counts as the text.

- lead_in: words before the first start match;
- tail: words after the last end match; absent when the case has no end pattern;
- pure_text: no lead-in and, where the end is known, no tail. A closing offer
  after a text without fixed last words shows only in closer, which also flags
  a "let me know" inside the text itself, so read those replies.

A pattern locates the point; it does not check that the point is correct.
Shape numbers are proxies for scanning, not evidence of reader comprehension.

--control CONDITION adds a constructed CONDITION+buried arm: each reply of that
condition gets a fixed warm-up paragraph and has all its blocks joined into one.
The metrics should mark that arm worse; if they do not, they cannot tell a buried
point from a stated one.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import statistics

WORD = re.compile(r'\w+')
FENCE = re.compile(r'```.*?```', re.S)
HEADING = re.compile(r'^\s{0,3}#{1,6}\s')
ITEM = re.compile(r'^\s*(?:[-*+•]|\d+[.)])\s+')
TABLE = re.compile(r'^\s*\|')
SENTENCE_END = re.compile(r'[.!?…](?=["»)\]*_]*(?:\s|$))')
FENCE_LINE = re.compile(r'^\s*```.*$', re.M)
QUESTION = re.compile(r'\?(?=["»)\]*_]*(?:\s|$))')
LABEL_LINE = re.compile(r'^\s*\*\*[^*]*[^*.!?…]\*\*:?\s*$')
LEAD_LABEL = re.compile(r'\*\*(?:\W*\w+){1,3}\W*\*\*')
GREETING = re.compile(
    r'^\s*(?:здравствуйте|добрый (?:день|вечер)|привет|hello|hi|dear|good (?:morning|afternoon))\b.{0,30}$',
    re.I)
OPENER = re.compile(
    r'^\W*(?:(?:отличный|хороший|интересный) вопрос|конечно|разумеется|давайте|'
    r'(?:great|good|excellent) question|sure\b|certainly|of course|absolutely|happy to|let\'?s)',
    re.I)
WRAPPER = re.compile(r'^\W*(?:вот\b|here\'?s\b|here is\b|вариант\b|draft\b|option\b)', re.I)
CLOSER = re.compile(
    r'если (?:хотите|нужно|потребуется|понадобится)|могу (?:также|ещё|помочь|подготовить)|'
    r'надеюсь|обращайтесь|дайте знать|хотите,? (?:я|чтобы)|'
    r'if you(?:\'d| would) like|let me know|hope this helps|feel free|i can also|'
    r'want me to|happy to help|would you like',
    re.I)
WARM_UP = {
    'ru': 'Хороший вопрос. Давайте спокойно разберёмся по порядку, что здесь происходит, '
          'какие есть условия и что из этого следует, чтобы ничего не упустить и не запутаться в деталях.',
    'en': 'Good question. Let us go through this calmly and in order, looking at what is happening here, '
          'which conditions apply and what follows from them, so that nothing gets missed along the way.',
}


def words(text):
    return len(WORD.findall(text))


def paragraphs(text):
    return [p for p in re.split(r'\n\s*\n', text.strip()) if p.strip()]


def blocks(text):
    """Units the eye meets as one piece: prose paragraphs, list items and table rows."""
    units = []
    for paragraph in paragraphs(text):
        lines = [line for line in paragraph.splitlines() if line.strip() and not HEADING.match(line)]
        if any(ITEM.match(line) or TABLE.match(line) for line in lines):
            units.extend(lines)
        elif lines:
            units.append(' '.join(lines))
    return units


def sentences(line):
    return [s for s in re.split(r'(?<=[.!?…])\s+', ITEM.sub('', line).strip()) if s]


def first_sentence_span(text):
    """Offsets of the first sentence in the reply.

    Headings, table rows, bold label lines ("**Submission rules**") and a greeting
    line ("Здравствуйте!") are skipped, as is a list marker. A bold lead-in of up to
    three words ("**Срок.**", "**No.**") is not a sentence on its own: the span runs
    on to the end of the next sentence.
    """
    offset = 0
    for line in text.splitlines(keepends=True):
        if (line.strip() and not HEADING.match(line) and not TABLE.match(line)
                and not LABEL_LINE.match(line) and not GREETING.match(line)):
            marker = ITEM.match(line)
            start = offset + (marker.end() if marker else len(line) - len(line.lstrip()))
            line_end = offset + len(line.rstrip('\n'))
            label = LEAD_LABEL.match(text, start, line_end)
            end = SENTENCE_END.search(text, label.end() if label else start, line_end)
            return start, end.end() if end else line_end
        offset += len(line)
    return 0, 0


def wrapping(text, spec):
    """Words around a requested ready text, located by its start and end patterns."""
    plain = FENCE_LINE.sub('', text)
    start = re.search(spec['start'], plain)
    if not start:
        return {'text_found': False}
    row = {'text_found': True, 'lead_in': words(plain[:start.start()])}
    if spec.get('end'):
        ends = list(re.finditer(spec['end'], plain[start.start():]))
        if not ends:
            return {'text_found': False}
        row['tail'] = words(plain[start.start() + ends[-1].end():])
    row['pure_text'] = not row['lead_in'] and not row.get('tail')
    return row


def measure(text, key=None, deliverable=None):
    prose = FENCE.sub(' ', text)
    lines = [line for line in prose.splitlines() if line.strip() and not HEADING.match(line)]
    start, end = first_sentence_span(prose)
    paras = paragraphs(prose)
    row = {
        'words': words(text),
        'longest_block': max((words(b) for b in blocks(prose)), default=0),
        'longest_sentence': max((words(s) for line in lines if not TABLE.match(line)
                                 for s in sentences(line)), default=0),
        'headings': sum(bool(HEADING.match(line)) for line in prose.splitlines()),
        'opener': bool(OPENER.match(prose[start:end])),
        'wrapper': bool(paras and WRAPPER.match(paras[0])),
        'closer': bool(paras and CLOSER.search(paras[-1])),
        'questions': len(QUESTION.findall(prose)),
    }
    if row['questions']:
        last = list(QUESTION.finditer(prose))[-1]
        row['after_question'] = words(prose[last.end():])
        row['question_last'] = not row['after_question']
    if key:
        found = re.search(key, prose)
        row['to_point'] = words(prose[:found.start()]) if found else words(prose)
        row['point_found'] = bool(found)
        row['point_first'] = bool(found and found.start() < end)
    if deliverable:
        row.update(wrapping(text, deliverable))
    return row


def bury(text, language):
    """A constructed bad reply: warm-up first, then every block joined into one wall."""
    flat = ' '.join(ITEM.sub('', line).strip() for line in text.splitlines()
                    if line.strip() and not HEADING.match(line))
    return WARM_UP[language] + '\n\n' + flat


def share_positive(rows, field):
    values = [r[field] for r in rows if field in r]
    return round(sum(v > 0 for v in values) / len(values), 3) if values else None


def summarize(rows):
    def median(field):
        values = [r[field] for r in rows if field in r]
        return statistics.median(values) if values else None

    def share(field):
        values = [r[field] for r in rows if field in r]
        return round(sum(values) / len(values), 3) if values else None

    keyed = [r for r in rows if 'to_point' in r]
    asked = [r for r in rows if r['questions']]
    return {
        'replies': len(rows),
        'keyed': len(keyed),
        'point_missed': sum(not r['point_found'] for r in keyed),
        'words': median('words'),
        'to_point': median('to_point'),
        'point_first': share('point_first'),
        'longest_block': median('longest_block'),
        'longest_sentence': median('longest_sentence'),
        'with_headings': round(sum(r['headings'] > 0 for r in rows) / len(rows), 3),
        'opener': share('opener'),
        'wrapper': share('wrapper'),
        'closer': share('closer'),
        'asked': round(len(asked) / len(rows), 3),
        'question_last': share('question_last'),
        'after_question': median('after_question'),
        'texts': sum(bool(r.get('text_found')) for r in rows),
        'text_missed': sum('text_found' in r and not r['text_found'] for r in rows),
        'pure_text': share('pure_text'),
        'lead_in': share_positive(rows, 'lead_in'),
        'tail': share_positive(rows, 'tail'),
    }


def evaluate(records, keys, control=None, split=None, deliverables=None):
    rows = []
    for record in records:
        language = record['case_id'].split('-', 1)[0]
        key = keys.get(record['case_id'])
        deliverable = (deliverables or {}).get(record['case_id'])
        variants = [(record['condition'], record['response'])]
        if record['condition'] == control:
            variants.append((control + '+buried', bury(record['response'], language)))
        for condition, text in variants:
            group = {'language': language, 'case': record['case_id']}.get(split)
            rows.append(((condition, group), measure(text, key, deliverable)))
    groups = {}
    for label, row in rows:
        groups.setdefault(label, []).append(row)
    return {label: summarize(group) for label, group in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1] or ''))}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('responses', help='JSON array in the blind_eval.py responses format')
    parser.add_argument('--keys', default=str(Path(__file__).with_name('answer-keys.json')))
    parser.add_argument('--control', metavar='CONDITION', help='add a constructed buried arm from this condition')
    parser.add_argument('--split', choices=('language', 'case'), help='group by language or case within each condition')
    parser.add_argument('--json', action='store_true', help='print JSON instead of a table')
    args = parser.parse_args()

    records = json.loads(Path(args.responses).read_text(encoding='utf-8'))
    key_file = json.loads(Path(args.keys).read_text(encoding='utf-8'))
    keys = key_file['keys']
    unknown = sorted({r['case_id'] for r in records} - set(keys))
    results = evaluate(records, keys, args.control, args.split, key_file.get('deliverables'))
    meta = {'responses_sha256': digest(args.responses), 'keys_sha256': digest(args.keys),
            'cases_without_key_entry': unknown}
    if args.json:
        print(json.dumps({'meta': meta, 'results': [{'condition': c, 'group': g, **s}
                                                    for (c, g), s in results.items()]},
                         ensure_ascii=False, indent=2))
        return
    for name, value in meta.items():
        print(f'{name}: {value}')
    columns = list(next(iter(results.values())))
    print('\t'.join(['condition', 'group'] + columns))
    for (condition, group), summary in results.items():
        print('\t'.join([condition, group or 'all'] + ['' if summary[c] is None else str(summary[c]) for c in columns]))


if __name__ == '__main__':
    main()
