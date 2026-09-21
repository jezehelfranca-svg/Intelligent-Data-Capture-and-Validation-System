from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import fitz

from engiverify.extraction.pdf import (
    analyze_pdf,
    extract_document_text,
    extract_native_blocks,
    extract_region,
)
from engiverify.ingestion.source import build_source_manifest
from engiverify.ocr.base import OcrUnavailableError
from engiverify.profiles import extract_profile_fields, validate_profile

class FakeOcrProvider:
    def is_available(self):
        return True

    def metadata(self):
        return {
            "provider": "fake_ocr",
            "engine_version": "test-1",
            "method": "ocr_fake",
        }

    def extract_image(self, image_bytes, *, page_number):
        return [{
            "text": f"Scanned page {page_number} shall provide a PAGA loudspeaker.",
            "bbox_px": [100, 120, 900, 220],
            "confidence": 0.88,
        }]

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

    def make_mixed_pdf(self, root):
        path=Path(root)/"mixed.pdf"
        doc=fitz.open()
        page1=doc.new_page()
        page1.insert_text((72,72),"Telecommunication system shall include CCTV.")
        doc.new_page()
        doc.save(path)
        doc.close()
        return path

    def test_native_pdf_analysis_and_blocks(self):
        with TemporaryDirectory() as td:
            path=self.make_pdf(td)
            analysis=analyze_pdf(path)
            self.assertEqual(analysis["page_count"],1)
            self.assertTrue(analysis["is_native_text"])
            self.assertFalse(analysis["ocr_required"])
            blocks=extract_native_blocks(path,source_document_id="SRC-1")
            self.assertGreaterEqual(len(blocks),1)
            self.assertTrue(all(b["page_number"]==1 for b in blocks))

    def test_mixed_pdf_routes_only_blank_page_to_ocr(self):
        with TemporaryDirectory() as td:
            path=self.make_mixed_pdf(td)
            analysis=analyze_pdf(path)
            self.assertTrue(analysis["mixed_content"])
            self.assertEqual(analysis["native_text_page_numbers"],[1])
            self.assertEqual(analysis["ocr_required_pages"],[2])

            fields=extract_document_text(
                path,
                source_document_id="SRC-MIX",
                ocr_provider=FakeOcrProvider(),
                dpi=200,
            )
            native=[f for f in fields if f["extraction_method"]=="native_pdf_block"]
            ocr=[f for f in fields if f["extraction_method"]=="ocr_fake"]
            self.assertTrue(native)
            self.assertEqual(len(ocr),1)
            self.assertEqual(ocr[0]["page_number"],2)
            self.assertEqual(ocr[0]["ocr_provider"],"fake_ocr")
            self.assertEqual(ocr[0]["ocr_engine_version"],"test-1")
            self.assertEqual(ocr[0]["ocr_confidence"],0.88)
            self.assertEqual(ocr[0]["review_status"],"REVIEW_REQUIRED")
            self.assertEqual(len(ocr[0]["bounding_box"]),4)

    def test_scanned_page_without_provider_fails_explicitly(self):
        with TemporaryDirectory() as td:
            path=self.make_mixed_pdf(td)
            with self.assertRaises(OcrUnavailableError):
                extract_document_text(path,source_document_id="SRC-MIX")

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
