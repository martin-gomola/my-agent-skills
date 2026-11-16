import importlib.util
import json
import shutil
import tempfile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name) / "repository"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "tmp", "dist", "__pycache__", ".venv"))

    def test_native_packages_keep_handoff_separate(self):
        validator.validate(self.root)
        self.assertEqual({p.name for p in (self.root / 'skills').iterdir()}, {'what-to-ask', 'your-turn-handoff', 'clean-cursor', 'pii-precommit-check', 'ask', 'codex-image', 'stop-slop'})
        for name in (p.name for p in (self.root / 'skills').iterdir() if p.is_dir()):
            self.assertEqual([p.parent.name for p in (self.root / 'plugins' / name / 'skills').glob('*/SKILL.md')], [name])

    def test_changed_snapshot_is_rejected_and_regenerated(self):
        snapshot = self.root / 'plugins/what-to-ask/skills/what-to-ask/SKILL.md'
        snapshot.write_text('stale')
        with self.assertRaisesRegex(ValueError, 'stale plugin snapshot'):
            validator.validate(self.root)
        validator.sync(self.root)
        validator.validate(self.root)

    def test_handoff_cannot_leak_into_other_plugin(self):
        extra = self.root / 'plugins/what-to-ask/skills/your-turn-handoff'
        shutil.copytree(self.root / 'skills/your-turn-handoff', extra)
        with self.assertRaisesRegex(ValueError, 'only its own skill'):
            validator.validate(self.root)

    def test_version_drift_is_rejected(self):
        manifest = self.root / "plugins/what-to-ask/.claude-plugin/plugin.json"
        data = json.loads(manifest.read_text())
        data["version"] = "99.0.0"
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "versions differ"):
            validator.validate(self.root)

    def test_installer_cannot_silently_select_the_other_plugin(self):
        path = self.root / 'site/catalog.json'
        catalog = json.loads(path.read_text())
        catalog['skills'][0]['plugin'] = 'your-turn-handoff'
        path.write_text(json.dumps(catalog))
        with self.assertRaisesRegex(ValueError, 'skill and plugin do not match'):
            validator.validate(self.root)

    def test_changed_provenance_requires_checksum_update(self):
        note = self.root / "skills/what-to-ask/tests/sources/dev-prompts-method.md"
        note.write_text(note.read_text() + "\nChanged\n")
        with self.assertRaisesRegex(ValueError, "checksum"):
            validator.validate(self.root)

    def test_private_content_is_rejected(self):
        private = self.root / "private.txt"
        private.write_text("/" + "Users" + "/example-user/private-file")
        with self.assertRaisesRegex(ValueError, "private path"):
            validator.validate(self.root)

    def test_standalone_skill_requires_its_license(self):
        (self.root / "skills/what-to-ask/LICENSE").unlink()
        with self.assertRaisesRegex(ValueError, "include a license"):
            validator.validate(self.root)


if __name__ == "__main__":
    unittest.main()
