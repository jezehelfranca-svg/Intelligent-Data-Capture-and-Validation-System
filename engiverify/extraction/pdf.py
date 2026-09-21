"""PDF analysis and coordinate-preserving native/OCR extraction."""
from pathlib import Path
import fitz

from engiverify.ocr.base import OcrUnavailableError


def analyze_pdf(path):
    pdf_path = Path(path)
    native_pages = []
    ocr_pages = []
    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc):
            page_no = page_index + 1
            if page.get_text("text").strip():
                native_pages.append(page_no)
            else:
                ocr_pages.append(page_no)
        return {
            "page_count": doc.page_count,
            "native_text_pages": len(native_pages),
            "native_text_page_numbers": native_pages,
            "ocr_required_pages": ocr_pages,
            "is_native_text": len(native_pages) > 0,
            "ocr_required": len(ocr_pages) > 0,
            "all_pages_require_ocr": len(ocr_pages) == doc.page_count and doc.page_count > 0,
            "mixed_content": bool(native_pages and ocr_pages),
        }


def _native_blocks_for_page(page, *, page_number: int, source_document_id: str):
    blocks = []
    for block_index, block in enumerate(page.get_text("blocks")):
        x0, y0, x1, y1, text = block[:5]
        block_type = block[6] if len(block) > 6 else 0
        if block_type != 0 or not str(text).strip():
            continue
        blocks.append({
            "extraction_id": f"{source_document_id}-P{page_number}-B{block_index + 1}",
            "source_document_id": source_document_id,
            "field_name": "__text_block__",
            "original_value": str(text).strip(),
            "page_number": page_number,
            "bounding_box": [float(x0), float(y0), float(x1), float(y1)],
            "extraction_method": "native_pdf_block",
            "extraction_confidence": 1.0,
            "ocr_provider": None,
            "ocr_engine_version": None,
            "ocr_confidence": None,
            "profile_id": None,
            "profile_version": None,
            "review_status": "UNREVIEWED",
        })
    return blocks


def extract_native_blocks(path, *, source_document_id: str):
    blocks = []
    with fitz.open(path) as doc:
        for page_index, page in enumerate(doc):
            blocks.extend(
                _native_blocks_for_page(
                    page,
                    page_number=page_index + 1,
                    source_document_id=source_document_id,
                )
            )
    return blocks


def _ocr_page(
    page,
    *,
    page_number: int,
    source_document_id: str,
    provider,
    dpi: int,
):
    if provider is None or not provider.is_available():
        raise OcrUnavailableError(
            f"Page {page_number} requires OCR but no available OCR provider is configured"
        )
    scale = float(dpi) / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    image_bytes = pix.tobytes("png")
    lines = provider.extract_image(image_bytes, page_number=page_number)
    metadata = provider.metadata() or {}
    x_scale = page.rect.width / pix.width if pix.width else 1.0
    y_scale = page.rect.height / pix.height if pix.height else 1.0

    out = []
    for line_index, line in enumerate(lines, start=1):
        text = str(line.get("text") or "").strip()
        bbox_px = line.get("bbox_px")
        if not text or not isinstance(bbox_px, (list, tuple)) or len(bbox_px) != 4:
            continue
        x0, y0, x1, y1 = [float(v) for v in bbox_px]
        confidence = line.get("confidence")
        confidence = None if confidence is None else max(0.0, min(1.0, float(confidence)))
        out.append({
            "extraction_id": f"{source_document_id}-P{page_number}-OCR-L{line_index}",
            "source_document_id": source_document_id,
            "field_name": "__text_line__",
            "original_value": text,
            "page_number": page_number,
            "bounding_box": [
                x0 * x_scale,
                y0 * y_scale,
                x1 * x_scale,
                y1 * y_scale,
            ],
            "extraction_method": metadata.get("method") or "ocr",
            "extraction_confidence": confidence,
            "ocr_provider": metadata.get("provider"),
            "ocr_engine_version": metadata.get("engine_version"),
            "ocr_confidence": confidence,
            "render_dpi": int(dpi),
            "profile_id": None,
            "profile_version": None,
            "review_status": "REVIEW_REQUIRED",
        })
    return out


def extract_document_text(
    path,
    *,
    source_document_id: str,
    ocr_provider=None,
    dpi: int = 200,
    min_native_chars: int = 1,
):
    """Extract native text where available and OCR only pages that need it.

    Mixed PDFs are supported page-by-page. OCR results always retain provider
    metadata, confidence, page number, and PDF-space bounding boxes.
    """
    if dpi < 72:
        raise ValueError("dpi must be >= 72")
    if min_native_chars < 1:
        raise ValueError("min_native_chars must be >= 1")

    results = []
    with fitz.open(path) as doc:
        for page_index, page in enumerate(doc):
            page_number = page_index + 1
            native_text = page.get_text("text").strip()
            if len(native_text) >= min_native_chars:
                results.extend(
                    _native_blocks_for_page(
                        page,
                        page_number=page_number,
                        source_document_id=source_document_id,
                    )
                )
            else:
                results.extend(
                    _ocr_page(
                        page,
                        page_number=page_number,
                        source_document_id=source_document_id,
                        provider=ocr_provider,
                        dpi=dpi,
                    )
                )
    return results


def extract_region(path, *, page_number: int, bbox):
    if page_number < 1:
        raise ValueError("page_number is 1-based and must be >= 1")
    if len(bbox) != 4:
        raise ValueError("bbox must contain [x0, y0, x1, y1]")
    rect = fitz.Rect(*[float(v) for v in bbox])
    with fitz.open(path) as doc:
        if page_number > doc.page_count:
            raise ValueError(f"page_number {page_number} exceeds PDF page count {doc.page_count}")
        page = doc[page_number - 1]
        return page.get_text("text", clip=rect).strip()
