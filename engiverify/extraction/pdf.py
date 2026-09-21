"""Native PDF analysis and coordinate-preserving extraction."""
from pathlib import Path
import fitz

def analyze_pdf(path):
    pdf_path = Path(path)
    with fitz.open(pdf_path) as doc:
        text_pages = 0
        for page in doc:
            if page.get_text("text").strip():
                text_pages += 1
        return {
            "page_count": doc.page_count,
            "native_text_pages": text_pages,
            "is_native_text": text_pages > 0,
            "ocr_required": text_pages == 0,
        }

def extract_native_blocks(path, *, source_document_id: str):
    blocks = []
    with fitz.open(path) as doc:
        for page_index, page in enumerate(doc):
            for block_index, block in enumerate(page.get_text("blocks")):
                x0, y0, x1, y1, text = block[:5]
                block_type = block[6] if len(block) > 6 else 0
                if block_type != 0 or not str(text).strip():
                    continue
                blocks.append({
                    "extraction_id": f"{source_document_id}-P{page_index + 1}-B{block_index + 1}",
                    "source_document_id": source_document_id,
                    "field_name": "__text_block__",
                    "original_value": str(text).strip(),
                    "page_number": page_index + 1,
                    "bounding_box": [float(x0), float(y0), float(x1), float(y1)],
                    "extraction_method": "native_pdf_block",
                    "extraction_confidence": 1.0,
                    "profile_id": None,
                    "profile_version": None,
                })
    return blocks

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
