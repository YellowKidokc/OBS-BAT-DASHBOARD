import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from tools.folder_snapshot import capture, render


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'Vault'
        for folder in ['.Road 02', 'Road 01/Empty', '.obsidian']:
            (self.root / folder).mkdir(parents=True)
        (self.root / '.Road 02/paper.md').write_text('Paper')
        (self.root / 'Road 01/paper.md').write_text('Other')
        (self.root / '.obsidian/private.json').write_text('DO NOT EMBED')

    def fingerprint(self):
        return {str(p.relative_to(self.root)): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
                for p in self.root.rglob('*') if p.is_file()}

    def test_inventory_is_read_only_and_includes_hidden_empty_boundaries(self):
        before = self.fingerprint()
        result = capture([self.root])
        self.assertEqual(before, self.fingerprint())
        self.assertTrue(result['complete'])
        root = result['roots'][0]
        self.assertEqual((root['files'], root['bytes']), (2, 10))
        self.assertEqual(root['folders'], 4)
        hidden = next(c for c in root['children'] if c['name'] == '.Road 02')
        self.assertTrue(hidden['hidden'])
        system = next(c for c in root['children'] if c['name'] == '.obsidian')
        self.assertTrue(system['excluded'])
        self.assertNotIn('DO NOT EMBED', render(result))
        self.assertEqual(capture([self.root], True)['roots'][0]['files'], 3)

    def test_symlinks_not_followed_and_missing_root_is_incomplete(self):
        (self.root / 'loop').symlink_to(self.root, target_is_directory=True)
        result = capture([self.root])
        self.assertEqual(result['roots'][0]['files'], 2)
        self.assertEqual(next(c for c in result['roots'][0]['children'] if c['name']=='loop')['kind'], 'boundary')
        self.assertFalse(capture([self.base/'missing'])['complete'])

    def test_overlapping_roots_rejected(self):
        with self.assertRaises(ValueError):
            capture([self.root, self.root/'Road 01'])

    def test_html_escapes_names(self):
        (self.root/'<script>alert(1)</script>'.replace('/', '_')).mkdir()
        report = render(capture([self.root]))
        self.assertIn('&lt;script&gt;', report)
        self.assertNotIn('<script>alert(1)', report)

    def test_cli_outputs_reports_and_refuses_overwrite_or_output_inside_root(self):
        script = str(Path(__file__).resolve().parents[1]/'tools/folder_snapshot.py')
        output = self.base/'report'
        args = [sys.executable, script, str(self.root), '--output', str(output)]
        first = subprocess.run(args, capture_output=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertTrue((output/'snapshot.html').is_file())
        self.assertTrue((output/'snapshot.json').is_file())
        self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)
        args[-1] = str(self.root/'report')
        self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)


if __name__ == '__main__':
    unittest.main()
