"""Each coding task must fail its hidden tests as given and pass them with the reference."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("code_tasks", Path(__file__).with_name("code_tasks.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class CodeTaskTests(unittest.TestCase):
    def test_task_folders_match_the_list(self):
        listed = {t["id"] for t in mod.tasks()}
        on_disk = {p.name for p in mod.TASKS.iterdir() if p.is_dir()}
        self.assertEqual(listed, on_disk)

    def test_start_fails_and_reference_passes(self):
        for task in mod.tasks():
            with self.subTest(task=task["id"]), tempfile.TemporaryDirectory() as tmp:
                work = Path(tmp) / "work"
                mod.prepare(task["id"], work)
                start = mod.score(task["id"], work)
                self.assertFalse(start["hidden"]["passed"])
                for source in (mod.TASKS / task["id"] / "reference").iterdir():
                    shutil.copy(source, work)
                solved = mod.score(task["id"], work)
                self.assertTrue(solved["hidden"]["passed"], solved)
                self.assertTrue(solved["visible"]["passed"], solved)
                self.assertGreater(solved["hidden"]["tests"], 0)

    def test_prepare_refuses_a_folder_with_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "x.txt").write_text("x")
            with self.assertRaises(SystemExit):
                mod.prepare("median", tmp)


if __name__ == "__main__":
    unittest.main()
