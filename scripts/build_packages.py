#!/usr/bin/env python3
"""Generate the committed host packages and catalogs from the standalone skill."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = 'packages'
REPOSITORY = 'https://github.com/ponomr/palych'
OWNER = {'name': 'ponomr', 'url': 'https://github.com/ponomr'}
KEYWORDS = ['writing', 'plain-language', 'russian', 'english', 'replies']
# The Claude Code mod ships from its own folder; its manifest is its source.
MOD = 'mods/palych-toggle'


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def text(value):
    return value.encode('utf-8')


def data(value):
    return text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def plugin_files(source, host, prefix, builder):
    """Collect a plugin built by build_plugin.py as {relative path: bytes}."""
    with tempfile.TemporaryDirectory() as temp:
        target = builder.build(source, Path(temp) / 'plugin', host)
        return {f'{prefix}/{path.relative_to(target).as_posix()}': path.read_bytes()
                for path in sorted(target.rglob('*')) if path.is_file()}


def render(source=ROOT):
    """Return every generated file as {relative path: bytes}."""
    builder, installer = load('build_plugin'), load('install')
    version, description = builder.VERSION, builder.DESCRIPTION
    rules = installer.payload(source)
    license_text = (source / 'LICENSE').read_bytes()
    files = {}
    files.update(plugin_files(source, 'claude-code', f'{PACKAGES}/claude-code', builder))
    files.update(plugin_files(source, 'codex', f'{PACKAGES}/codex', builder))

    # Cursor has no session hooks; an always-applied rule keeps the core active.
    cursor = f'{PACKAGES}/cursor'
    files[f'{cursor}/.cursor-plugin/plugin.json'] = data({
        'name': 'palych', 'displayName': 'Palych', 'version': version,
        'description': description, 'author': OWNER, 'homepage': REPOSITORY,
        'repository': REPOSITORY, 'license': 'MIT', 'keywords': KEYWORDS})
    files[f'{cursor}/rules/palych.mdc'] = text(
        '---\ndescription: Palych compact, clear replies\n'
        'alwaysApply: true\n---\n\n' + rules)
    files[f'{cursor}/LICENSE'] = license_text

    # The canonical skill folder is what Hermes and `npx skills add` install by
    # GitHub path; `hermes -s palych` preloads it.
    files[f'{builder.SKILL.as_posix()}/LICENSE'] = license_text

    entry = {'name': 'palych', 'description': description, 'version': version}
    mod = json.loads((source / MOD / '.claude-plugin' / 'plugin.json').read_text(encoding='utf-8'))
    files['.claude-plugin/marketplace.json'] = data({
        'name': 'palych', 'owner': OWNER,
        'metadata': {'description': description, 'version': version},
        'plugins': [{**entry, 'source': f'./{PACKAGES}/claude-code', 'author': OWNER,
                     'homepage': REPOSITORY, 'repository': REPOSITORY, 'license': 'MIT',
                     'keywords': KEYWORDS, 'category': 'productivity'},
                    {'name': mod['name'], 'description': mod['description'],
                     'version': mod['version'], 'source': f'./{MOD}', 'author': OWNER,
                     'homepage': REPOSITORY, 'repository': REPOSITORY, 'license': 'MIT',
                     'category': 'productivity'}]})
    files['.agents/plugins/marketplace.json'] = data({
        'name': 'palych', 'interface': {'displayName': 'Palych'},
        'plugins': [{'name': 'palych',
                     'source': {'source': 'local', 'path': f'./{PACKAGES}/codex'},
                     'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                     'category': 'Productivity'}]})
    files['.cursor-plugin/marketplace.json'] = data({
        'name': 'palych', 'owner': OWNER,
        'metadata': {'description': description, 'version': version},
        'plugins': [{'name': 'palych', 'source': f'./{PACKAGES}/cursor', 'description': description}]})
    return dict(sorted(files.items()))


def drift(root=ROOT):
    """List generated files that are missing, changed or no longer produced."""
    expected = render(root)
    problems = []
    for relative, content in expected.items():
        path = root / relative
        if not path.is_file() or path.is_symlink():
            problems.append(f'{relative}: missing generated file')
        elif path.read_bytes() != content:
            problems.append(f'{relative}: differs from source; run scripts/build_packages.py')
    if (root / PACKAGES).exists():
        for path in sorted((root / PACKAGES).rglob('*')):
            relative = path.relative_to(root).as_posix()
            if path.is_file() and relative not in expected and '__pycache__' not in path.parts:
                problems.append(f'{relative}: not produced by scripts/build_packages.py')
    return problems


def write(root=ROOT):
    expected = render(root)
    # packages/ is fully generated, so stale files are removed with the old tree.
    if (root / PACKAGES).exists():
        shutil.rmtree(root / PACKAGES)
    for relative, content in expected.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='report drift without writing')
    args = parser.parse_args()
    if args.check:
        problems = drift()
        if problems:
            print('\n'.join(problems), file=sys.stderr)
            return 1
        print('Generated packages match the source.')
        return 0
    print(f'Wrote {write()} generated files.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
