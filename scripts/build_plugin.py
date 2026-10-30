#!/usr/bin/env python3
"""Build an optional plugin from the standalone skill; do not install it."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

VERSION = '0.9.0'
SKILL = Path('skills/palych')
ADAPTER_DOCS = 'https://github.com/ponomr/palych/blob/main/adapters/README.md'
DESCRIPTION = 'Clear conversational replies in Russian and English, enabled by default with persistent mode controls.'


def build(source, target, host):
    if target.exists():
        raise ValueError('output already exists; choose a new path')
    target.parent.mkdir(parents=True, exist_ok=True)
    # Validate the complete source inventory before writing a partial package.
    inventory = [source / SKILL / 'SKILL.md', source / 'LICENSE', source / 'adapters/session_hook.py',
                 source / 'assets/icon.png']
    inventory += list((source / SKILL / 'references').glob('*.md'))
    for path in inventory:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'not a regular source file: {path.name}')
    staging = Path(tempfile.mkdtemp(prefix='.palych-', dir=target.parent))
    try:
        skill = staging / 'skills' / 'palych'
        skill.mkdir(parents=True)
        for path in (source / SKILL / 'references').glob('*.md'):
            (skill / 'references').mkdir(exist_ok=True)
            shutil.copy2(path, skill / 'references' / path.name)
        # Redirect the adapter pointer to the bundled docs; development protocols
        # are intentionally absent from the runtime core.
        body = (source / SKILL / 'SKILL.md').read_text(encoding='utf-8')
        body = body.replace(f'({ADAPTER_DOCS})', '(../../README.md)')
        (skill / 'SKILL.md').write_text(body, encoding='utf-8')
        shutil.copy2(source / 'LICENSE', staging / 'LICENSE')
        shutil.copy2(source / 'adapters/README.md', staging / 'README.md')
        hooks = staging / 'hooks'
        hooks.mkdir()
        shutil.copy2(source / 'adapters/session_hook.py', hooks / 'session_hook.py')
        env = 'PLUGIN_ROOT' if host == 'codex' else 'CLAUDE_PLUGIN_ROOT'
        handler = {'type': 'command', 'command': f'python3 "${{{env}}}/hooks/session_hook.py" --host {host}', 'timeout': 10}
        # The full core is deliberately restored after compaction. Codex's default
        # hook output threshold could spill it; this bound keeps this small skill inline.
        if host == 'codex':
            handler['additionalContextLimit'] = 6000
        config = {'hooks': {
            'SessionStart': [{'matcher': '^(startup|resume|clear|compact|fork)$', 'hooks': [handler]}],
            'UserPromptSubmit': [{'hooks': [handler]}],
        }}
        (hooks / 'hooks.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
        directory = staging / ('.codex-plugin' if host == 'codex' else '.claude-plugin')
        directory.mkdir()
        manifest = {'name': 'palych', 'version': VERSION, 'description': DESCRIPTION,
                    'author': {'name': 'ponomr', 'url': 'https://github.com/ponomr'},
                    'homepage': 'https://github.com/ponomr/palych',
                    'repository': 'https://github.com/ponomr/palych',
                    'license': 'MIT', 'skills': './skills/'}
        if host == 'claude-code':
            # Claude's directory reads the default .claude-plugin/icon.png (square PNG, 512-2048 px).
            shutil.copy2(source / 'assets/icon.png', directory / 'icon.png')
        (directory / 'plugin.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        staging.rename(target)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=('codex', 'claude-code'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    try:
        print(build(source, args.output.expanduser().resolve(), args.host))
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
