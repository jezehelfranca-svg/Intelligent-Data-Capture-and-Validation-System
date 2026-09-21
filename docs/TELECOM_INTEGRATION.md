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

Page-level OCR routing is implemented through a provider interface. The first provider is local Tesseract CLI. Mixed PDFs are processed page-by-page: native-text pages remain native extraction, while scanned pages use OCR.

OCR output preserves provider/version metadata, OCR confidence, render DPI, source page, and PDF-space bounding boxes. OCR results remain review-required evidence. If OCR is needed and no provider is available, extraction fails explicitly instead of silently returning blank data.

See [OCR Processing](OCR.md).

## Confidentiality

Real client/vendor documents must not be committed to this public repository. The code and tests generate synthetic files at runtime.
