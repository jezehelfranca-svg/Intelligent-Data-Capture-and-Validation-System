"""Stable interchange bundle for downstream telecom engineering systems."""
from datetime import datetime, timezone
from engiverify import __version__

SCHEMA_VERSION = "engiverify.telecom.v1"

def build_telecom_bundle(*, project_id: str, source_documents, extracted_fields):
    source_ids = {str(d.get("source_document_id")) for d in source_documents}
    if not source_ids or None in source_ids:
        raise ValueError("Every source document requires source_document_id")
    seen = set()
    for field in extracted_fields:
        extraction_id = str(field.get("extraction_id") or "")
        if not extraction_id:
            raise ValueError("Every extracted field requires extraction_id")
        if extraction_id in seen:
            raise ValueError(f"Duplicate extraction_id: {extraction_id}")
        seen.add(extraction_id)
        if str(field.get("source_document_id")) not in source_ids:
            raise ValueError(f"Extracted field references unknown source: {field.get('source_document_id')}")
        if field.get("page_number") is not None and int(field["page_number"]) < 1:
            raise ValueError("page_number must be 1-based")
    return {
        "schema_version": SCHEMA_VERSION,
        "producer": {"name": "EngiVerify", "version": __version__},
        "project_id": project_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_documents": list(source_documents),
        "extracted_fields": list(extracted_fields),
        "authority": "human_validation_required",
    }

def validate_telecom_bundle(bundle):
    if bundle.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"Unsupported schema_version: {bundle.get('schema_version')}")
    rebuilt = build_telecom_bundle(
        project_id=bundle.get("project_id"),
        source_documents=bundle.get("source_documents") or [],
        extracted_fields=bundle.get("extracted_fields") or [],
    )
    return {
        "valid": True,
        "source_document_count": len(rebuilt["source_documents"]),
        "extracted_field_count": len(rebuilt["extracted_fields"]),
        "authority": rebuilt["authority"],
    }
