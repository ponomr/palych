#!/usr/bin/env python3
"""Prepare and score the small coding tasks in code-tasks/.

prepare copies a task's start/ files into an empty folder for the agent; the
hidden tests stay here. score copies the agent's folder, adds the hidden tests
and runs them with the visible ones, so the agent's own files are not changed.
Scoring runs the agent's code: use it only on folders from a sandboxed run.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

TASKS = Path(__file__).with_name('code-tasks')
RAN = re.compile(r'^Ran (\d+) tests?', re.M)
FAILED = re.compile(r'^FAILED \((.*)\)$', re.M)


def tasks():
    return json.loads((TASKS / 'tasks.json').read_text(encoding='utf-8'))['tasks']


def prepare(task_id, dest):
    dest = Path(dest)
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f'{dest} is not empty')
    shutil.copytree(TASKS / task_id / 'start', dest, dirs_exist_ok=True)


def run_tests(folder, module, timeout):
    try:
        proc = subprocess.run([sys.executable, '-m', 'unittest', module], cwd=folder,
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'passed': False, 'tests': None, 'problems': 'timeout'}
    ran = RAN.search(proc.stderr)
    failed = FAILED.search(proc.stderr)
    return {'passed': proc.returncode == 0 and bool(ran),
            'tests': int(ran.group(1)) if ran else None,
            'problems': failed.group(1) if failed else ('' if proc.returncode == 0 else 'error')}


def score(task_id, workdir, timeout=60):
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / 'work'
        shutil.copytree(workdir, folder, ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy(TASKS / task_id / 'hidden' / 'test_hidden.py', folder)
        return {'task': task_id,
                'hidden': run_tests(folder, 'test_hidden', timeout),
                'visible': run_tests(folder, 'test_visible', timeout)}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare', help='copy a task into an empty folder')
    p.add_argument('task')
    p.add_argument('dest')
    s = sub.add_parser('score', help='run hidden and visible tests on a copy of a folder')
    s.add_argument('task')
    s.add_argument('workdir')
    sub.add_parser('list', help='print task ids')
    args = parser.parse_args()
    if args.command == 'list':
        print('\n'.join(t['id'] for t in tasks()))
    elif args.command == 'prepare':
        prepare(args.task, args.dest)
    else:
        print(json.dumps(score(args.task, args.workdir), ensure_ascii=False))


if __name__ == '__main__':
    main()
