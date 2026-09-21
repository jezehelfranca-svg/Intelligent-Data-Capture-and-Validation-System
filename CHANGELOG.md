# Changelog

## 0.2.0 — 2026-09-21

### Added
- Page-level native/OCR routing for mixed and scanned PDFs.
- Pluggable OCR provider contract.
- Local Tesseract CLI provider with TSV coordinate/confidence parsing.
- OCR provider/version/confidence/render-DPI metadata in telecom extraction records.
- Explicit failure when OCR is required but no provider is available.

### Preserved
- Immutable source handling.
- Native PDF extraction.
- Workbook ingestion.
- Document profiles.
- `engiverify.telecom.v1` compatibility.
- Human validation as final authority.
