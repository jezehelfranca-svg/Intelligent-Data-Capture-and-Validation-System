"""Versioned document-profile validation and deterministic region extraction."""
from copy import deepcopy

_ALLOWED_STATUS = {"DRAFT", "UNDER_VALIDATION", "APPROVED", "RETIRED"}

def validate_profile(profile):
    required = ["profile_id", "name", "version", "document_type", "status", "fields"]
    missing = [key for key in required if key not in profile]
    if missing:
        raise ValueError(f"Profile missing required fields: {', '.join(missing)}")
    if profile["status"] not in _ALLOWED_STATUS:
        raise ValueError(f"Unsupported profile status: {profile['status']}")
    if not isinstance(profile["fields"], list) or not profile["fields"]:
        raise ValueError("Profile must contain at least one field definition")
    names = set()
    for field in profile["fields"]:
        for key in ["field_name", "page_number", "bbox"]:
            if key not in field:
                raise ValueError(f"Profile field missing {key}")
        if field["field_name"] in names:
            raise ValueError(f"Duplicate profile field: {field['field_name']}")
        names.add(field["field_name"])
        if int(field["page_number"]) < 1:
            raise ValueError("Profile page_number must be 1-based")
        if len(field["bbox"]) != 4:
            raise ValueError("Profile bbox must contain four coordinates")
    return deepcopy(profile)

def extract_profile_fields(pdf_path, *, source_manifest, profile):
    from engiverify.extraction.pdf import extract_region
    profile = validate_profile(profile)
    results = []
    for index, field in enumerate(profile["fields"], start=1):
        value = extract_region(
            pdf_path,
            page_number=int(field["page_number"]),
            bbox=field["bbox"],
        )
        results.append({
            "extraction_id": f"{source_manifest['source_document_id']}-{profile['profile_id']}-{index}",
            "source_document_id": source_manifest["source_document_id"],
            "field_name": field["field_name"],
            "original_value": value,
            "page_number": int(field["page_number"]),
            "bounding_box": [float(v) for v in field["bbox"]],
            "extraction_method": "profile_region_native_pdf",
            "extraction_confidence": 1.0 if value else 0.0,
            "profile_id": profile["profile_id"],
            "profile_version": profile["version"],
            "data_type": field.get("data_type", "string"),
            "unit": field.get("unit"),
            "review_status": "REVIEW_REQUIRED" if not value else "UNREVIEWED",
        })
    return results
