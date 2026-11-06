"""Generated host packages follow the standalone skill and stay in sync with it."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('packages', ROOT / 'scripts/build_packages.py')
packages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packages)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.files = packages.render(ROOT)

    def content(self, path):
        return self.files[path].decode('utf-8')

    def test_always_on_hosts_get_the_same_core(self):
        core = packages.load('rules').payload(ROOT)
        rule = self.content('packages/cursor/rules/palych.mdc')
        self.assertTrue(rule.startswith('---\ndescription: '))
        self.assertIn('\nalwaysApply: true\n---\n\n', rule)
        self.assertTrue(rule.endswith(core))

    def test_catalogs_point_at_generated_packages(self):
        claude = json.loads(self.content('.claude-plugin/marketplace.json'))
        codex = json.loads(self.content('.agents/plugins/marketplace.json'))
        cursor = json.loads(self.content('.cursor-plugin/marketplace.json'))
        sources = [claude['plugins'][0]['source'], codex['plugins'][0]['source']['path'],
                   cursor['plugins'][0]['source']]
        for source in sources:
            relative = source.removeprefix('./')
            self.assertNotIn('..', relative)
            self.assertTrue(any(path == relative or path.startswith(relative + '/')
                                for path in self.files), source)

    def test_claude_catalog_lists_the_band_mod(self):
        claude = json.loads(self.content('.claude-plugin/marketplace.json'))
        mod = next(p for p in claude['plugins'] if p['name'] == 'palych-toggle')
        manifest = json.loads((ROOT / mod['source'] / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual((mod['version'], mod['description']), (manifest['version'], manifest['description']))

    def test_skill_folder_is_self_contained(self):
        skill = (ROOT / 'skills/palych/SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('](adapters/', skill)
        self.assertNotIn('](../', skill)
        self.assertIn('skills/palych/LICENSE', self.files)
        self.assertFalse(any(path.startswith('packages/hermes/') for path in self.files))

    def test_drift_reports_changed_extra_and_missing_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ('skills', 'LICENSE', 'adapters', 'assets', 'scripts', 'mods'):
                source = ROOT / name
                (shutil.copytree if source.is_dir() else shutil.copy2)(source, root / name)
            module_spec = importlib.util.spec_from_file_location('copy', root / 'scripts/build_packages.py')
            copy = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(copy)
            copy.write(root)
            self.assertEqual(copy.drift(root), [])
            (root / 'packages/cursor/rules/palych.mdc').write_text('edited\n', encoding='utf-8')
            (root / 'packages/extra.txt').write_text('stale\n', encoding='utf-8')
            (root / '.cursor-plugin/marketplace.json').unlink()
            problems = '\n'.join(copy.drift(root))
            self.assertIn('packages/cursor/rules/palych.mdc: differs', problems)
            self.assertIn('packages/extra.txt: not produced', problems)
            self.assertIn('.cursor-plugin/marketplace.json: missing', problems)


if __name__ == '__main__':
    unittest.main()
