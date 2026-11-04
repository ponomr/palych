"""Installer tests use isolated configuration directories, never personal settings."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.config = self.base / 'config with spaces'
        self.config.mkdir()

    def test_install_update_remove_preserve_existing_bytes_for_both_hosts(self):
        original = b'# Existing rules\r\nKeep my instructions.\r\n'
        for host, name in [('codex', 'AGENTS.md'), ('claude-code', 'CLAUDE.md')]:
            with self.subTest(host=host):
                path = self.config / name
                path.write_bytes(original)
                first = installer.change(self.config, host, 'install')
                self.assertEqual(Path(first['backup']).read_bytes(), original)
                self.assertEqual(Path(first['backup']).stat().st_mode & 0o777, 0o600)
                self.assertTrue(path.read_bytes().endswith(original))
                self.assertTrue(installer.change(self.config, host, 'check')['installed'])
                self.assertFalse(installer.change(self.config, host, 'install')['changed'])
                installer.change(self.config, host, 'uninstall')
                self.assertEqual(path.read_bytes(), original)
                self.assertFalse(installer.change(self.config, host, 'uninstall')['changed'])

    def test_new_config_contains_runtime_rules_without_a_skill_call(self):
        installer.change(self.config, 'codex', 'install')
        text = (self.config / 'AGENTS.md').read_text()
        runtime = (ROOT / installer.SKILL / 'SKILL.md').read_text().split('---', 2)[2]
        self.assertIn(runtime.split('## Activation and scope', 1)[0].strip(), text)
        self.assertIn('every chat reply', text)
        self.assertIn('explicit request to turn it off takes priority', text)
        self.assertNotIn('## Optional examples', text)
        self.assertNotIn('references/examples.ru.md', text)
        self.assertNotIn('references/examples.en.md', text)
        self.assertEqual((self.config / 'AGENTS.md').stat().st_mode & 0o777, 0o600)

    def test_optional_examples_do_not_remove_the_final_runtime_check(self):
        required = '# Palych\n\nKeep exact values.\n\nCheck claims before sending.\n'
        for optional in (
            '## Optional examples\nRead [RU](references/examples.ru.md).\n',
            'Consult only relevant optional\n[RU](references/examples.ru.md).\n',
        ):
            with self.subTest(optional=optional):
                source = self.base / 'source'
                (source / installer.SKILL).mkdir(parents=True, exist_ok=True)
                (source / installer.SKILL / 'SKILL.md').write_text(
                    '---\nname: palych\n---\n\n' + required + optional)
                block = installer.block(source)
                self.assertIn(required, block)
                self.assertNotIn('references/examples.ru.md', block)

    def test_updated_source_replaces_block_once(self):
        installer.change(self.config, 'codex', 'install')
        source = self.base / 'source'
        (source / installer.SKILL).mkdir(parents=True)
        updated = (ROOT / installer.SKILL / 'SKILL.md').read_text().replace(
            '# Palych\n', '# Palych\n\nSynthetic revised instruction.\n', 1)
        (source / installer.SKILL / 'SKILL.md').write_text(updated)
        installer.change(self.config, 'codex', 'install', source)
        text = (self.config / 'AGENTS.md').read_text()
        self.assertEqual(text.count(installer.START), 1)
        self.assertIn('Synthetic revised instruction.', text)
        with self.assertRaises(ValueError):
            installer.change(self.config, 'codex', 'check')

    def test_codex_existing_override_is_used_without_touching_base(self):
        base = self.config / 'AGENTS.md'
        base.write_text('Base rules.')
        override = self.config / 'AGENTS.override.md'
        override.write_text('Override rules.')
        installer.change(self.config, 'codex', 'install')
        self.assertEqual(base.read_text(), 'Base rules.')
        self.assertTrue(override.read_text().endswith('Override rules.'))

    def test_linked_files_and_edited_blocks_are_preserved(self):
        path = self.config / 'AGENTS.md'
        other = self.base / 'owned.md'
        other.write_text('Owner rules.')
        path.symlink_to(other)
        with self.assertRaises(ValueError):
            installer.change(self.config, 'codex', 'install')
        self.assertEqual(other.read_text(), 'Owner rules.')
        path.unlink()
        installer.change(self.config, 'codex', 'install')
        installed = path.read_text()
        self.assertEqual(installed.count(installer.END), 1)
        path.write_text(installed.replace(installer.END, 'Owner edit.\n' + installer.END, 1))
        edited = path.read_bytes()
        self.assertNotEqual(edited, installed.encode('utf-8'))
        for action in ('install', 'uninstall', 'check'):
            with self.assertRaises(ValueError):
                installer.change(self.config, 'codex', action)
            self.assertEqual(path.read_bytes(), edited)

    def test_failed_atomic_replace_preserves_existing_file_and_backup(self):
        path = self.config / 'CLAUDE.md'
        path.write_text('Keep this.')
        with patch.object(installer.os, 'replace', side_effect=OSError('simulated failure')):
            with self.assertRaises(OSError):
                installer.change(self.config, 'claude-code', 'install')
        self.assertEqual(path.read_text(), 'Keep this.')
        self.assertEqual(len(list((self.config / '.palych-backups').iterdir())), 1)
        self.assertFalse(list(self.config.glob('.palych-*md')))

    def test_cli_respects_custom_config_environment_and_check_does_not_write(self):
        for host, env, name in [('codex', 'CODEX_HOME', 'AGENTS.md'),
                                ('claude-code', 'CLAUDE_CONFIG_DIR', 'CLAUDE.md')]:
            config = self.base / host
            environment = dict(os.environ, **{env: str(config)})
            command = [sys.executable, str(ROOT / 'scripts/install.py')]
            result = subprocess.run(command + ['check', '--host', host], env=environment, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(config.exists())
            for action in ('install', 'check', 'uninstall'):
                result = subprocess.run(command + [action, '--host', host], env=environment, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((config / name).read_bytes(), b'')


if __name__ == '__main__':
    unittest.main()
