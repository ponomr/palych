#!/usr/bin/env python3
"""Install Palych as global reply instructions; no network or third-party packages."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import uuid

START = '<!-- palych:start -->\n'
END = '<!-- palych:end -->\n\n'
STAMP = re.compile(r'<!-- palych:sha256 ([0-9a-f]{64}) -->\n')
ROOT = Path(__file__).resolve().parents[1]
SKILL = Path('skills/palych')
ADAPTER_DOCS = 'https://github.com/ponomr/palych/blob/main/adapters/README.md'


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def payload(source=ROOT):
    """Return the always-on instructions shared by global installs and host packages."""
    core = (source / SKILL / 'SKILL.md').read_text(encoding='utf-8')
    # Optional examples and installation links are not needed in global context.
    body = core.split('---', 2)[2].split('## Optional examples', 1)[0]
    # The compact core keeps its optional pointer after the final self-check.
    body = body.split('Consult only relevant optional', 1)[0].strip()
    body = body.replace(f'[host adapter]({ADAPTER_DOCS})', 'host adapter')
    return ('Palych is enabled by default for every chat reply in this conversation.\n'
               'An explicit request to turn it off takes priority until enabled again.\n'
               'Keep the current on/off state when compacting or handing off context.\n\n'
               + body + '\n')


def block(source=ROOT):
    text = payload(source)
    return START + '<!-- palych:sha256 ' + digest(text) + ' -->\n' + text + END


def locate(text):
    if 'palych:start' not in text and 'palych:end' not in text:
        return None
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('malformed Palych block; inspect it before changing instructions')
    start = text.index(START)
    end = text.index(END, start) + len(END)
    stamp = STAMP.match(text, start + len(START))
    if not stamp or digest(text[stamp.end():end - len(END)]) != stamp.group(1):
        raise ValueError('Palych block was edited; preserve your edits before replacing it')
    return start, end


def target(config, host):
    if host == 'codex':
        override = config / 'AGENTS.override.md'
        if override.exists() or override.is_symlink():
            return override
        return config / 'AGENTS.md'
    return config / 'CLAUDE.md'


def read(path):
    if path.is_symlink() or (path.exists() and path.stat().st_nlink != 1):
        raise ValueError('instruction file is linked; use its managing workflow instead')
    if path.exists() and not path.is_file():
        raise ValueError('instruction path is not a regular file')
    return path.read_bytes() if path.exists() else b''


@contextmanager
def locked(config):
    config.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = config / '.palych-install.lock'
    if path.is_symlink():
        raise ValueError('installer lock is a symlink')
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, 'a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def change(config, host, action, source=ROOT):
    path = target(config, host)
    original = read(path)
    text = original.decode('utf-8')
    span = locate(text)
    desired = block(source)
    if action == 'check':
        if not span or text[span[0]:span[1]] != desired:
            raise ValueError('current Palych rules are not installed in global instructions')
        return {'installed': True, 'path': str(path), 'changed': False}
    if action == 'install':
        updated = (text[:span[0]] + desired + text[span[1]:]) if span else desired + text
    else:
        updated = (text[:span[0]] + text[span[1]:]) if span else text
    if updated == text:
        return {'installed': action == 'install', 'path': str(path), 'changed': False}
    backup = None
    if path.exists():
        folder = config / '.palych-backups'
        if folder.is_symlink():
            raise ValueError('backup directory is a symlink')
        folder.mkdir(mode=0o700, exist_ok=True)
        backup = folder / (uuid.uuid4().hex + '-' + path.name)
        fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(original)
            stream.flush()
            os.fsync(stream.fileno())
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
    fd, temporary = tempfile.mkstemp(prefix='.palych-', dir=config)
    try:
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(updated.encode('utf-8'))
            stream.flush()
            os.fsync(stream.fileno())
        if read(path) != original:
            raise ValueError('instruction file changed during installation; retry after reviewing it')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    result = {'installed': action == 'install', 'path': str(path), 'changed': True}
    if backup:
        result['backup'] = str(backup)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('install', 'check', 'uninstall'))
    parser.add_argument('--host', required=True, choices=('codex', 'claude-code'))
    parser.add_argument('--config-dir', type=Path, help='override the host configuration directory')
    args = parser.parse_args()
    env = 'CODEX_HOME' if args.host == 'codex' else 'CLAUDE_CONFIG_DIR'
    default = Path.home() / ('.codex' if args.host == 'codex' else '.claude')
    config = (args.config_dir or Path(os.environ.get(env) or default)).expanduser().absolute()
    try:
        if args.action == 'check':
            result = change(config, args.host, args.action)
        else:
            with locked(config):
                result = change(config, args.host, args.action)
        print(json.dumps(result))
        return 0
    except (OSError, ValueError, UnicodeError, IndexError) as error:
        print(f'Palych installer: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
