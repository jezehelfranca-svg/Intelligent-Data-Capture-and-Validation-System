"""OCR provider contracts.

OCR is optional at runtime. A provider must expose availability, metadata, and
coordinate-bearing text-line extraction. Results remain review candidates.
"""

class OcrUnavailableError(RuntimeError):
    """Raised when a page requires OCR but no configured provider is available."""


class OcrProvider:
    def is_available(self) -> bool:
        raise NotImplementedError

    def metadata(self) -> dict:
        raise NotImplementedError

    def extract_image(self, image_bytes: bytes, *, page_number: int) -> list[dict]:
        """Return OCR line dictionaries with text, bbox_px and confidence."""
        raise NotImplementedError
