"""Failure-injection checks for the packaging integrity boundary."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import verify as v


class PortableChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / 'payload.txt'
        self.file.write_bytes(b'unchanged')
        manifest = {'source_manifest_sha256': v.SOURCE_SHA, 'files': {
            'payload.txt': {'bytes': 9, 'sha256': hashlib.sha256(b'unchanged').hexdigest()}}}
        (self.root / 'package-manifest.json').write_text(json.dumps(manifest))

    def test_original_fixture_passes(self):
        v.check_manifest(self.root)

    def test_changed_bytes_fail_even_when_length_matches(self):
        self.file.write_bytes(b'tampered!')
        with self.assertRaisesRegex(ValueError, 'hash/size mismatch'):
            v.check_manifest(self.root)

    def test_missing_file_fails(self):
        self.file.unlink()
        with self.assertRaisesRegex(ValueError, 'file set'):
            v.check_manifest(self.root)

    def test_unlisted_file_fails(self):
        (self.root / 'unlisted.txt').write_text('extra')
        with self.assertRaisesRegex(ValueError, 'file set'):
            v.check_manifest(self.root)

    def test_symlink_fails_even_with_matching_content(self):
        other = self.root / 'target'
        self.file.rename(other)
        self.file.symlink_to(other)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            v.check_manifest(self.root)

    def test_duplicate_json_key_fails(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
            json.loads('{"cases":713,"cases":712}', object_pairs_hook=v.unique)

    def test_receipt_exclusions_cannot_hide_changed_counts(self):
        with self.assertRaisesRegex(ValueError, 'receipt changed: cases'):
            v.compare_volatile_receipt({'at':'new','cases':712}, {'at':'old','cases':713}, {'at'}, 'test')

    def test_receipt_exclusions_cannot_hide_new_fields(self):
        with self.assertRaisesRegex(ValueError, 'fields changed'):
            v.compare_volatile_receipt({'at':'new','extra':True}, {'at':'old'}, {'at'}, 'test')


if __name__ == '__main__':
    unittest.main()
