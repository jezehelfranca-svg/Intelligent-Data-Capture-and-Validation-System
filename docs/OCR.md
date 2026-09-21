# OCR Processing

EngiVerify supports page-level OCR routing for scanned and mixed PDFs.

## Provider model

OCR is pluggable. The first provider is the local Tesseract command-line engine.

- Native-text pages continue to use PyMuPDF text blocks.
- Pages with no usable native text are rendered to PNG and sent to the OCR provider.
- OCR word coordinates are grouped into text lines.
- Pixel coordinates are converted back to PDF-space bounding boxes.
- Provider name, engine version, OCR confidence, render DPI, page number, and bounding box are retained.

OCR results remain review candidates. They are never auto-approved based on confidence.

## Tesseract

The Python package does not bundle the Tesseract executable. Install Tesseract through the operating system or approved enterprise software distribution and ensure `tesseract` is on PATH.

The provider can be instantiated as:

```python
from engiverify.ocr import TesseractCliProvider
from engiverify.extraction.pdf import extract_document_text

provider = TesseractCliProvider(languages="eng", psm=6)
fields = extract_document_text(
    "specification.pdf",
    source_document_id="SRC-001",
    ocr_provider=provider,
)
```

If a page requires OCR and no provider is available, EngiVerify raises an explicit `OcrUnavailableError`; it does not silently return an empty extraction.

## Confidentiality

This provider runs locally. Cloud OCR providers are not enabled by this implementation. Any future cloud provider must undergo data-residency, confidentiality, access-control, retention, and security review before project use.
