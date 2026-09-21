import unittest
from engiverify.interchange import build_telecom_bundle, validate_telecom_bundle

class BundleTests(unittest.TestCase):
    def test_bundle_preserves_source_evidence(self):
        docs=[{"source_document_id":"SRC-1","sha256":"a"*64}]
        fields=[{
            "extraction_id":"EXT-1","source_document_id":"SRC-1","field_name":"ip_rating",
            "original_value":"IP66","page_number":4,"bounding_box":[1,2,3,4],
            "extraction_method":"profile_region_native_pdf","extraction_confidence":1.0,
            "profile_id":"P1","profile_version":"1"
        }]
        bundle=build_telecom_bundle(project_id="SYN",source_documents=docs,extracted_fields=fields)
        result=validate_telecom_bundle(bundle)
        self.assertTrue(result["valid"])
        self.assertEqual(result["extracted_field_count"],1)
        self.assertEqual(bundle["authority"],"human_validation_required")

    def test_unknown_source_reference_rejected(self):
        with self.assertRaises(ValueError):
            build_telecom_bundle(
                project_id="SYN",
                source_documents=[{"source_document_id":"SRC-1"}],
                extracted_fields=[{"extraction_id":"E1","source_document_id":"SRC-X","page_number":1}]
            )

if __name__=="__main__":
    unittest.main()
