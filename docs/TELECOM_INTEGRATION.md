# Telecom Integration Contract

EngiVerify owns source-document ingestion and evidence capture. Downstream telecom engineering repositories should consume its structured outputs rather than duplicate PDF/OCR logic.

## Ownership boundary

```text
PDF / XLSX / CSV
      ↓
EngiVerify
  - source hash
  - immutable source identity
  - page / bbox evidence
  - document profile
  - raw extracted value
      ↓
engiverify.telecom.v1
      ↓
Telecom_Career_Path
  - requirement review
  - vendor datasheet attribute mapping
  - traceability
  - compliance/reconciliation
      ↓
Telecom_MTO / vendor / ITB digital thread
```

## Bundle rules

A bundle contains:

- producer name/version
- project ID
- exact source-document manifests
- extracted fields with source document ID
- 1-based page number
- bounding box
- original extracted value
- extraction method/confidence
- profile ID/version when a profile was used

The bundle deliberately does not declare contractual compliance or final engineering acceptance.

## Document profiles

The current executable profile supports deterministic page/rectangle extraction from native-text PDFs. Profiles are versioned and status-controlled.

An unvalidated profile may be used to generate review candidates, but it must not be treated as approved engineering configuration.

## OCR

OCR is not implemented in the first executable foundation. `analyze_pdf()` explicitly reports `ocr_required=true` for PDFs with no native text. A future OCR provider must preserve coordinates, provider/version metadata, confidence, and human-review status.

## Confidentiality

Real client/vendor documents must not be committed to this public repository. The code and tests generate synthetic files at runtime.
