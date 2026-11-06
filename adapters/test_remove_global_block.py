"""Migration and rule tests use isolated configuration directories, never personal settings."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'scripts/{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


remover = load('remove_global_block')
rules = load('rules')


def legacy_block(body='Old Palych rules.\n'):
    """The block format releases before 0.10.0 wrote into global instructions."""
    return (remover.START + f'<!-- palych:sha256 {remover.digest(body)} -->\n'
            + body + remover.END)


class RemoveGlobalBlockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.config = self.base / 'config with spaces'
        self.config.mkdir()

    def test_remove_restores_owner_bytes_and_keeps_a_private_backup(self):
        owner = b'# Existing rules\r\nKeep my instructions.\r\n'
        for host, name in [('codex', 'AGENTS.md'), ('claude-code', 'CLAUDE.md')]:
            with self.subTest(host=host):
                path = self.config / name
                installed = legacy_block().encode('utf-8') + owner
                path.write_bytes(installed)
                path.chmod(0o640)
                self.assertEqual(remover.run(self.config, host, 'check'), {'global_block': [str(path)]})
                self.assertEqual(path.read_bytes(), installed)
                removed = remover.run(self.config, host, 'remove')['removed']
                self.assertEqual(len(removed), 1)
                self.assertEqual(path.read_bytes(), owner)
                self.assertEqual(path.stat().st_mode & 0o777, 0o640)
                saved = Path(removed[0]['backup'])
                self.assertEqual(saved.read_bytes(), installed)
                self.assertEqual(saved.stat().st_mode & 0o777, 0o600)
                self.assertEqual(remover.run(self.config, host, 'remove'), {'removed': []})
                self.assertEqual(remover.run(self.config, host, 'check'), {'global_block': []})

    def test_files_without_a_block_are_untouched(self):
        path = self.config / 'CLAUDE.md'
        path.write_text('Owner rules.')
        self.assertEqual(remover.run(self.config, 'claude-code', 'remove'), {'removed': []})
        self.assertEqual(path.read_text(), 'Owner rules.')
        self.assertFalse((self.config / '.palych-backups').exists())

    def test_codex_override_and_base_are_both_cleaned(self):
        base = self.config / 'AGENTS.md'
        override = self.config / 'AGENTS.override.md'
        base.write_text(legacy_block() + 'Base rules.')
        override.write_text(legacy_block() + 'Override rules.')
        found = remover.run(self.config, 'codex', 'check')['global_block']
        self.assertEqual(sorted(found), sorted([str(base), str(override)]))
        remover.run(self.config, 'codex', 'remove')
        self.assertEqual(base.read_text(), 'Base rules.')
        self.assertEqual(override.read_text(), 'Override rules.')

    def test_edited_malformed_and_linked_blocks_are_refused_without_writing(self):
        path = self.config / 'AGENTS.md'
        edited = legacy_block().replace(remover.END, 'Owner edit.\n' + remover.END, 1)
        for text in (edited, remover.START + 'no stamp or end\n',
                     legacy_block() + legacy_block()):
            with self.subTest(text=text[:40]):
                path.write_text(text)
                for action in ('check', 'remove'):
                    with self.assertRaises(ValueError):
                        remover.run(self.config, 'codex', action)
                    self.assertEqual(path.read_text(), text)
        path.unlink()
        other = self.base / 'owned.md'
        other.write_text(legacy_block())
        path.symlink_to(other)
        with self.assertRaises(ValueError):
            remover.run(self.config, 'codex', 'remove')
        self.assertEqual(other.read_text(), legacy_block())

    def test_failed_atomic_replace_preserves_existing_file_and_backup(self):
        path = self.config / 'CLAUDE.md'
        path.write_text(legacy_block() + 'Keep this.')
        with patch.object(remover.os, 'replace', side_effect=OSError('simulated failure')):
            with self.assertRaises(OSError):
                remover.run(self.config, 'claude-code', 'remove')
        self.assertEqual(path.read_text(), legacy_block() + 'Keep this.')
        self.assertEqual(len(list((self.config / '.palych-backups').iterdir())), 1)
        self.assertFalse(list(self.config.glob('.palych-*md')))

    def test_cli_respects_custom_config_and_check_does_not_write(self):
        for host, env, name in [('codex', 'CODEX_HOME', 'AGENTS.md'),
                                ('claude-code', 'CLAUDE_CONFIG_DIR', 'CLAUDE.md')]:
            with self.subTest(host=host):
                config = self.base / host
                environment = dict(os.environ, **{env: str(config)})
                command = [sys.executable, str(ROOT / 'scripts/remove_global_block.py')]
                for action in ('check', 'remove'):
                    result = subprocess.run(command + [action, '--host', host], env=environment,
                                            capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(config.exists())
                config.mkdir()
                (config / name).write_text(legacy_block() + 'Owner.')
                result = subprocess.run(command + ['check', '--host', host], env=environment,
                                        capture_output=True)
                self.assertEqual(result.returncode, 1)
                self.assertFalse((config / '.palych-backups').exists())
                result = subprocess.run(command + ['remove', '--host', host], env=environment,
                                        capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((config / name).read_text(), 'Owner.')
                result = subprocess.run(command + ['check', '--host', host, '--config-dir', str(config)],
                                        capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_no_script_writes_host_instruction_files(self):
        self.assertFalse((ROOT / 'scripts/install.py').exists())
        for script in (ROOT / 'scripts').glob('*.py'):
            if script.name == 'remove_global_block.py':
                continue
            text = script.read_text(encoding='utf-8')
            for name in ('CLAUDE.md', 'AGENTS.override.md', 'developer_instructions'):
                self.assertNotIn(name, text, f'{script.name} names {name}')


class RuleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def test_rule_contains_runtime_rules_without_optional_examples(self):
        text = rules.payload(ROOT)
        runtime = (ROOT / rules.SKILL / 'SKILL.md').read_text().split('---', 2)[2]
        self.assertIn('every chat reply', text)
        self.assertIn('explicit request to turn it off takes priority', text)
        self.assertNotIn('## Optional examples', text)
        self.assertNotIn('references/examples.ru.md', text)
        self.assertNotIn('references/examples.en.md', text)
        self.assertIn('## Repair and self-check', text)
        self.assertTrue(runtime.split('## Activation and scope', 1)[0].strip().startswith('# Palych'))

    def test_optional_examples_do_not_remove_the_final_runtime_check(self):
        required = '# Palych\n\nKeep exact values.\n\nCheck claims before sending.\n'
        for optional in (
            '## Optional examples\nRead [RU](references/examples.ru.md).\n',
            'Consult only relevant optional\n[RU](references/examples.ru.md).\n',
        ):
            with self.subTest(optional=optional):
                source = self.base / 'source'
                (source / rules.SKILL).mkdir(parents=True, exist_ok=True)
                (source / rules.SKILL / 'SKILL.md').write_text('---\nname: palych\n---\n\n' + required + optional)
                text = rules.payload(source)
                self.assertIn(required, text)
                self.assertNotIn('references/examples.ru.md', text)

    def test_rule_drops_plugin_only_text_only(self):
        text = rules.payload(ROOT)
        core = (ROOT / rules.SKILL / 'SKILL.md').read_text()
        for plugin_only in ('saved: true', 'host adapter', 'Hosts control', 'No tools or other skills required',
                            'not trusted adapter metadata'):
            self.assertIn(plugin_only, core)
            self.assertNotIn(plugin_only, text)
        for kept in ('turns Palych off for\nthis conversation only', 'search for no helper; honor the',
                     'Artifacts, including reusable text in chat', '## Repair and self-check'):
            self.assertIn(kept, text)

    def test_changed_activation_text_fails_the_build(self):
        source = self.base / 'source'
        (source / rules.SKILL).mkdir(parents=True)
        changed = (ROOT / rules.SKILL / 'SKILL.md').read_text().replace('`saved: true`', '`saved: yes`')
        (source / rules.SKILL / 'SKILL.md').write_text(changed)
        with self.assertRaises(ValueError):
            rules.payload(source)


if __name__ == '__main__':
    unittest.main()
