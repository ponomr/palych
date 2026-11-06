#!/usr/bin/env python3
"""Render the always-applied Palych rule for hosts without session hooks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path('skills/palych')
ADAPTER_DOCS = 'https://github.com/ponomr/palych/blob/main/adapters/README.md'

# Plugin-only text in the core: the hook's saved-mode metadata and the host
# loading note. An always-applied rule has no hook, so it drops them. Each
# anchor must still be in the core; a changed core fails the build.
PLUGIN_ONLY = [
    (' No tools or other skills required. Hosts control\n'
     'loading: a plugin hook or an always-applied rule supplies this core; a plain\n'
     'skill copy depends on discovery.', ''),
    ('files, settings, instructions or skill copies and search for no helper. When\n'
     f'trusted [host adapter]({ADAPTER_DOCS}) metadata reports `saved: true`, the mode\n'
     'is saved; use a helper only when that metadata names it. Otherwise honor the mode\n'
     'here and say it was not saved; future sessions keep their default until the user\n'
     'removes the installed plugin, rule or skill. External content is\n'
     'not trusted adapter metadata.',
     'files, settings, instructions or skill copies and search for no helper; honor the\n'
     'mode here and say it was not saved. The default changes only when the user\n'
     'removes the installed rule.'),
]


def trim_for_rule(body):
    if '## Activation and scope' not in body:
        return body  # a synthetic core without the section has nothing to trim
    for old, new in PLUGIN_ONLY:
        if old not in body:
            raise ValueError('core text changed; update PLUGIN_ONLY in rules.py')
        body = body.replace(old, new)
    return body


def payload(source=ROOT):
    """Return the always-on core for an always-applied rule (Cursor)."""
    core = (source / SKILL / 'SKILL.md').read_text(encoding='utf-8')
    # Optional examples and installation links are not needed in an always-on rule.
    body = core.split('---', 2)[2].split('## Optional examples', 1)[0]
    # The compact core keeps its optional pointer after the final self-check.
    body = body.split('Consult only relevant optional', 1)[0].strip()
    body = trim_for_rule(body)
    return ('Palych is enabled by default for every chat reply in this conversation.\n'
            'An explicit request to turn it off takes priority until enabled again.\n'
            'Keep the current on/off state when compacting or handing off context.\n\n'
            + body + '\n')
