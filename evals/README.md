# Evaluation / Проверка

The input sets are [single-turn prompts](prompts.json) and
[session probes](session-probes.json). They contain only synthetic public inputs.
Use the [rubric](rubric.md) for assessment and record results in
[observations](observations.md).

The additional [compactness regression set](compact-prompts.json) contains
20 original cases, ten per language. It checks task-specific reply shapes,
unsupported causes and system guarantees, cache conditions, exact restrictions,
and retention of requested options and depth. Its case criteria are in the rubric.
The original 20-case set and its historical evidence remain unchanged.

The [focused compactness set](compactness-prompts.json) adds 12 synthetic cases,
six per language: cache measurements, detailed processes, full comparisons with
unknown prices, failed checks, exact restrictions and progress updates. For a
bounded pilot, use two fresh replies per case and condition; add the existing
RU/EN `cost` and `depth` cases when testing the known repetition defects. Generate
both controls anew. Two repetitions are exploratory, below the full protocol.
Lock masked judgments before disclosure, then separately audit source meaning.
Report core size, native input/output tokens, output size and editorial preferences
separately. Smaller instructions or answers do not establish better understanding
or reduced subscription-limit debits.

`cache_usage.py` estimates from local Claude Code and Codex logs how often an
always-on core is read from the prompt cache and its average price relative to
uncached input. It prints aggregates only; record its output in the development
log with the date, window and revision.

`session_replies.py` compares visible reply length, output tokens and prose
slash chains in local Claude Code sessions started before and after a cutover,
such as the core's installation. It is observational: tasks, models and other
loaded instructions differ between periods. It prints aggregates only.

`shape_metrics.py` measures reply shape without an LLM judge: words before the
point, whether the point is in the first sentence, the longest unbroken block and
sentence, headings, and deliverable wrappers, ceremonial openers and closing offers.
It reads a responses file in the `blind_eval.py` format. The point is located by
the case's pattern in [answer-keys.json](answer-keys.json); write keys for new cases
from the prompt alone and record the key file's hash before scoring. A pattern
locates the point but does not check it, and it misses paraphrases, so read the
replies it marks. `--control CONDITION` adds a constructed buried arm that the
metrics must score worse. It also counts questions: the share of replies that
ask one, whether the reply ends with its question and how many words follow the
last question. Shape numbers are not reader comprehension.

The [ready-text set](deliverable-prompts.json) has eight synthetic RU/EN cases
that ask for a letter, a chat message, a commit message or a notice. It checks
that the reply is the text itself, with no lead-in before it and no comment or
offer after it. `answer-keys.json` gives each case patterns for the text's first
and last words; `shape_metrics.py` reports `lead_in`, `tail` and `pure_text`.

The [coding tasks](code-tasks/tasks.json) check that Palych does not hurt agent
work: eight small Python tasks, half of them bug fixes, with visible tests for the
agent and hidden tests kept back. `code_tasks.py prepare` copies a task into an
empty folder; `code_tasks.py score` runs the hidden and visible tests on a copy
of the agent's folder. Every behavior a hidden test checks is stated in the
task's prompt, and `test_code_tasks.py` checks that the starting files fail the
hidden tests and the reference solution passes them.

The [repetition set](repetition-prompts.json) checks semantic duplicates,
unambiguous referents and repetitive colon links. Use it alongside detailed
process, full-comparison and exact-condition cases; shortening cannot hide
missing stages, changed actors or lost conditions. The rubric treats synonym
cycling and punctuation counts as different from useful compactness. The next
candidate is prepared from one owner-supplied human-preferred example; it has
not undergone a new model run or a reader comprehension study.
Give generators only each case's `prompt`; `protected` criteria stay with the
assessor. Exact colons in URLs and quoted messages remain protected literals.

The [unknown-actor set](unknown-actor-prompts.json) has four synthetic RU/EN cases
with impersonal or passive wording: a price change and a closed folder whose actor
and reason are unknown. Use it with the unknown-reason and optional-backup cases.

The [reassurance set](reassurance-prompts.json) has four synthetic RU/EN cases on
optional actions with unknown consequences. Use it with the unknown-reason cases;
it checks that "optional" does not become "safe to skip".

The [empty-moves set](empty-moves-prompts.json) adds 12 synthetic RU/EN cases:
grading labels and placeholder explanations, causal chains under shortening,
price and count bounds, conflicting supplied facts, a plainly reported failure
and a legitimate contrast with a stated claim. Its candidate failed a masked pilot
and was dropped; the set remains for the recorded evidence.

The [label-reference set](label-reference-prompts.json) has four synthetic RU/EN
cases: a progress report on numbered steps and a report on a numbered option
chosen earlier. It checks that a label or number is not the only description.
Its candidate failed a masked pilot; the current core passed every case.

The [warning-order set](warning-order-prompts.json) has six synthetic RU/EN
cases: a router reset and an account deletion whose irreversible effect is
stated after the step, and a dark-theme guard with no warning. It checks that
the reader learns the effect before the step and that no warning is invented.
Its candidate failed a masked pilot; the current core put the warning after the
step in every reply.

The [blocking-question set](blocking-question-prompts.json) has ten synthetic
RU/EN progress cases. In six, work waits on the reader's decision: a currency
value, a conflicting date or a spending limit. In four, nothing is needed from
the reader. It checks that a needed decision is named in the first sentence, that
the reply ends with that one question, and that no question is invented when
nothing blocks the work. Its keys locate the decision, not the facts; score it
with `shape_metrics.py` and read the replies for the protected facts. Its
candidate was integrated on 2026-10-29.

The label-reference and blocking-question cases ask for a message to the user, so
each prompt names the reply language. Without it, English prompts got Russian
replies, with or without the core (2026-10-29 language probe in
[STATUS-LOG](../docs/history/STATUS-LOG.md)).

The [bounds and conflicts set](bounds-conflicts-prompts.json) has eight synthetic
RU/EN cases: price and count bounds, "at least"/"at most" limits, and conflicting
delivery terms or prices. Use it with the unknown-reason, roles and deadline cases.

The [full-comparison set](full-comparison-prompts.json) adds six synthetic RU/EN
cases: complete option lists, an unknown qualifying price, and a two-sentence
choice-only request. Repeat each case three times per condition. Check individual
values and uncertainty before presentation; record answer placement separately
from clarity judgments. Choice-only requests do not require a full table.

For a focused pilot select affected families; for a full run of the additional
set, pass `--prompts evals/compact-prompts.json` to the existing masking tool.
Three repetitions make 60 pairs for this set. Generation consumes the agent's
usage limits; run the free offline package checks first. Record new results in
distinct files. Focused model checks and their limits are recorded separately in
[development log](../docs/history/STATUS-LOG.md); historical results remain unchanged.

## Reproducible blind checks

Use [blind-protocol.md](blind-protocol.md) and `blind_eval.py` for new comparisons.
The full set has 20 cases (14 Russian, 6 English); run each three times in each
condition. Use fresh generation contexts per case when possible. Record shared
contexts and any unavailable settings rather than claiming independence.
The helper masks conditions, balances A/B positions, validates pairs, locks
judgments before disclosure, and reports semantic regressions separately.

The original results below remain historical editorial smoke tests; do not
relabel them as blind or as a controlled comparison. Model scoring still measures
editorial proxies, not reader comprehension. Use the separate
[reader protocol](reader-check.md) for that claim.

Record language compliance separately and use the rubric's assessor calibration.
Give the assessor only judging criteria and calibration, keeping later workflow
steps out of its prompt. An assessor's claim that it performed an unblinded audit
is not evidence of that audit; verify the actual inputs and recorded operations.
Audit verdicts against raw replies after locking; keep the audit separate from
the locked score. A missed error is not repaired by silently changing an earlier
judgment. Label any later audit as unblinded and record the exact tested core hash.

## Paired reply checks

1. Select the same case IDs for both conditions. Include Russian and English.
2. Keep the model, generation settings, tools, and base instructions the same.
   Start a fresh conversation for each case when the host allows it. In a
   batched smoke test, record that the cases share a context.
3. For the baseline, provide only the case's prompt. For the skill condition,
   load only `SKILL.md`, then provide the same prompt. Do not provide the
   rubric, examples, expected answer, or the paired response to either generator.
4. Save the raw outputs with the condition and case ID outside the public
   package. If generation or settings are unavailable, record that limitation;
   do not fabricate a baseline or claim a model setting you did not observe.
5. Mask the condition labels and vary their order for assessment where possible.
   Assess semantic preservation before style. Use content criteria rather than
   matching phrases or counting words.
6. Record ties and regressions as well as improvements. Revise demonstrated
   weaknesses, then rerun the affected cases. Retain earlier results.

This protocol can be run manually with the host's existing conversation tools.
The skill has no runtime evaluator or API dependency. External paid evaluation
is optional and requires its own budget and authorization.

## Session behavior

Use `session-probes.json` in a conversation where the host actually loads the
skill. Send one turn at a time. Check topic changes, a one-reply format override,
the artifact boundary, and explicit disabling. Record the observed behavior and
the host's context-retention limits. A single batched completion cannot prove
persistence or disabling.

## Reader comprehension / Понимание читателями

Проверяйте с читателями, для которых предназначен ответ. Учитывайте их знания
темы и заявленные потребности в чтении; не делайте предположений о диагнозе.

Дайте ответ без дополнительных пояснений. Попросите пересказать основную
мысль, ответить на конкретный вопрос из рубрики и отметить непонятные места.
Не ограничивайтесь вопросом «Понятно?». Разделяйте впечатление от стиля и
правильное понимание содержания.

Запишите ошибки понимания, измените объяснение и повторите проверку.
Самопроверка агента и оценка другим агентом не заменяют участие читателей.
Для любой сохранённой обратной связи согласуйте использование и публикацию;
не включайте личные ответы читателей в публичный пакет по умолчанию.

## Recording evidence

Report the tested revision or content hash, date, case IDs, observed generator
settings, conditions, limitations, semantic failures, and the type of evaluation.
Distinguish packaging checks, editorial review, agent behavior, and reader
comprehension. An instruction-only revision remains unverified until tested.

## Persistence evidence

Run the optional adapter checks with synthetic events:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s adapters -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_*.py'
```

Test enable → compact → off → compact with the always-on default active, in
separate processes sharing only saved state. Also test language changes, ordinary
prompts, quoted control phrases, corrupt state, and another session's isolation.
For a live-host integration check follow [adapter instructions](../adapters/README.md).
Record the host version and delivered hook context; a clear-looking reply is not
evidence that the hook ran. Live installation and real compaction remain a
separate verification step.
