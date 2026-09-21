from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from engiverify.core.hashing import sha256_bytes, sha256_file
from engiverify.ingestion.source import build_source_manifest, safe_filename, store_immutable

class HashAndSourceTests(unittest.TestCase):
    def test_hash_file_matches_bytes(self):
        with TemporaryDirectory() as td:
            path=Path(td)/"a.txt"
            path.write_bytes(b"abc")
            self.assertEqual(sha256_file(path), sha256_bytes(b"abc"))

    def test_filename_blocks_path_traversal(self):
        self.assertEqual(safe_filename("../../vendor sheet.pdf"), "vendor sheet.pdf")

    def test_manifest_and_immutable_copy(self):
        with TemporaryDirectory() as td:
            root=Path(td)
            source=root/"source.pdf"
            source.write_bytes(b"synthetic pdf bytes")
            manifest=build_source_manifest(source,project_id="SYN",document_type="vendor_datasheet",document_revision="A")
            self.assertEqual(len(manifest["sha256"]),64)
            dest=store_immutable(source,root/"store")
            self.assertTrue(dest.exists())
            self.assertEqual(sha256_file(dest),manifest["sha256"])
            self.assertEqual(store_immutable(source,root/"store"),dest)

if __name__=="__main__":
    unittest.main()
