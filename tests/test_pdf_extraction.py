from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import fitz

from engiverify.extraction.pdf import analyze_pdf, extract_native_blocks, extract_region
from engiverify.ingestion.source import build_source_manifest
from engiverify.profiles import extract_profile_fields, validate_profile

class PdfExtractionTests(unittest.TestCase):
    def make_pdf(self, root):
        path=Path(root)/"sheet.pdf"
        doc=fitz.open()
        page=doc.new_page()
        page.insert_text((72,72),"Model: PTZ-500")
        page.insert_text((72,112),"IP Rating: IP66")
        doc.save(path)
        doc.close()
        return path

    def test_native_pdf_analysis_and_blocks(self):
        with TemporaryDirectory() as td:
            path=self.make_pdf(td)
            analysis=analyze_pdf(path)
            self.assertEqual(analysis["page_count"],1)
            self.assertTrue(analysis["is_native_text"])
            blocks=extract_native_blocks(path,source_document_id="SRC-1")
            self.assertGreaterEqual(len(blocks),1)
            self.assertTrue(all(b["page_number"]==1 for b in blocks))

    def test_region_and_profile_extraction(self):
        with TemporaryDirectory() as td:
            path=self.make_pdf(td)
            text=extract_region(path,page_number=1,bbox=[60,45,300,90])
            self.assertIn("PTZ-500",text)
            manifest=build_source_manifest(path,project_id="SYN",document_type="vendor_datasheet",document_revision="A")
            profile={
                "profile_id":"P1","name":"Synthetic","version":"1","document_type":"vendor_datasheet","status":"DRAFT",
                "fields":[{"field_name":"model","page_number":1,"bbox":[60,45,300,90],"data_type":"string","unit":None}]
            }
            validate_profile(profile)
            fields=extract_profile_fields(path,source_manifest=manifest,profile=profile)
            self.assertIn("PTZ-500",fields[0]["original_value"])
            self.assertEqual(fields[0]["profile_id"],"P1")

    def test_duplicate_profile_fields_rejected(self):
        profile={"profile_id":"P","name":"x","version":"1","document_type":"x","status":"DRAFT",
                 "fields":[
                     {"field_name":"x","page_number":1,"bbox":[0,0,1,1]},
                     {"field_name":"x","page_number":1,"bbox":[0,0,1,1]}
                 ]}
        with self.assertRaises(ValueError):
            validate_profile(profile)

if __name__=="__main__":
    unittest.main()
