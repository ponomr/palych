#!/usr/bin/env python3
"""Find or remove the Palych block that releases before 0.10.0 wrote into global
instructions. Palych no longer writes host instruction files; no network access."""
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


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def locate(text):
    """Return the span of an intact stamped block, None without one."""
    if 'palych:start' not in text and 'palych:end' not in text:
        return None
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('malformed Palych block; inspect it by hand')
    start = text.index(START)
    end = text.index(END, start) + len(END)
    stamp = STAMP.match(text, start + len(START))
    if not stamp or digest(text[stamp.end():end - len(END)]) != stamp.group(1):
        raise ValueError('Palych block was edited; keep your edits and remove it by hand')
    return start, end


def targets(config, host):
    # Codex reads AGENTS.override.md in place of AGENTS.md; an old block may sit in either.
    names = ('AGENTS.override.md', 'AGENTS.md') if host == 'codex' else ('CLAUDE.md',)
    return [config / name for name in names]


def read(path):
    if path.is_symlink() or (path.exists() and path.stat().st_nlink != 1):
        raise ValueError(f'{path} is linked; change it through its managing workflow')
    if path.exists() and not path.is_file():
        raise ValueError(f'{path} is not a regular file')
    return path.read_bytes() if path.exists() else None


@contextmanager
def locked(config):
    path = config / '.palych-install.lock'
    if path.is_symlink():
        raise ValueError('lock is a symlink')
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, 'a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def backup(config, path, original):
    folder = config / '.palych-backups'
    if folder.is_symlink():
        raise ValueError('backup directory is a symlink')
    folder.mkdir(mode=0o700, exist_ok=True)
    copy = folder / (uuid.uuid4().hex + '-' + path.name)
    fd = os.open(copy, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(original)
        stream.flush()
        os.fsync(stream.fileno())
    return copy


def strip(config, path, original, span):
    text = original.decode('utf-8')
    updated = text[:span[0]] + text[span[1]:]
    saved = backup(config, path, original)
    fd, temporary = tempfile.mkstemp(prefix='.palych-', dir=config)
    try:
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), stat.S_IMODE(path.stat().st_mode))
            stream.write(updated.encode('utf-8'))
            stream.flush()
            os.fsync(stream.fileno())
        if read(path) != original:
            raise ValueError(f'{path} changed during removal; retry after reviewing it')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return saved


def run(config, host, action):
    found, removed = [], []
    for path in targets(config, host):
        original = read(path)
        if original is None:
            continue
        span = locate(original.decode('utf-8'))
        if span is None:
            continue
        if action == 'check':
            found.append(str(path))
        else:
            removed.append({'path': str(path), 'backup': str(strip(config, path, original, span))})
    if action == 'check':
        return {'global_block': found}
    return {'removed': removed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'remove'))
    parser.add_argument('--host', required=True, choices=('codex', 'claude-code'))
    parser.add_argument('--config-dir', type=Path, help='override the host configuration directory')
    args = parser.parse_args()
    env = 'CODEX_HOME' if args.host == 'codex' else 'CLAUDE_CONFIG_DIR'
    default = Path.home() / ('.codex' if args.host == 'codex' else '.claude')
    config = (args.config_dir or Path(os.environ.get(env) or default)).expanduser().absolute()
    try:
        if args.action == 'check' or not config.is_dir():
            # A missing config directory holds no block; nothing to lock or remove.
            result = run(config, args.host, args.action)
        else:
            with locked(config):
                result = run(config, args.host, args.action)
        print(json.dumps(result))
        # check exits 1 while a block is left, so a script can stop on it.
        return 1 if result.get('global_block') else 0
    except (OSError, ValueError, UnicodeError) as error:
        print(f'Palych: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
