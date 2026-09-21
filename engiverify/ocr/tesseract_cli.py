"""Local Tesseract CLI OCR provider with TSV coordinate extraction."""
from __future__ import annotations

import csv
import io
from pathlib import Path
import shutil
import subprocess
import tempfile

from engiverify.ocr.base import OcrProvider


def parse_tesseract_tsv(tsv_text: str) -> list[dict]:
    """Group Tesseract word-level TSV rows into coordinate-bearing text lines."""
    reader = csv.DictReader(io.StringIO(tsv_text), delimiter="\t")
    groups = {}
    order = []
    for row in reader:
        text = str(row.get("text") or "").strip()
        if not text:
            continue
        try:
            level = int(row.get("level") or 0)
        except ValueError:
            continue
        if level != 5:
            continue
        try:
            key = (
                int(row.get("block_num") or 0),
                int(row.get("par_num") or 0),
                int(row.get("line_num") or 0),
            )
            left = int(float(row.get("left") or 0))
            top = int(float(row.get("top") or 0))
            width = int(float(row.get("width") or 0))
            height = int(float(row.get("height") or 0))
            conf_raw = float(row.get("conf") or -1)
        except (TypeError, ValueError):
            continue
        if key not in groups:
            groups[key] = {
                "words": [],
                "x0": left,
                "y0": top,
                "x1": left + width,
                "y1": top + height,
                "confidences": [],
            }
            order.append(key)
        g = groups[key]
        g["words"].append(text)
        g["x0"] = min(g["x0"], left)
        g["y0"] = min(g["y0"], top)
        g["x1"] = max(g["x1"], left + width)
        g["y1"] = max(g["y1"], top + height)
        if conf_raw >= 0:
            g["confidences"].append(conf_raw)

    lines = []
    for key in order:
        g = groups[key]
        confidence = None
        if g["confidences"]:
            confidence = max(0.0, min(1.0, sum(g["confidences"]) / len(g["confidences"]) / 100.0))
        lines.append({
            "text": " ".join(g["words"]).strip(),
            "bbox_px": [g["x0"], g["y0"], g["x1"], g["y1"]],
            "confidence": confidence,
            "line_key": list(key),
        })
    return lines


class TesseractCliProvider(OcrProvider):
    def __init__(self, *, languages: str = "eng", psm: int = 6, executable: str | None = None):
        self.languages = languages
        self.psm = int(psm)
        self.executable = executable or shutil.which("tesseract")

    def is_available(self) -> bool:
        return bool(self.executable and Path(self.executable).exists())

    def _version(self) -> str | None:
        if not self.is_available():
            return None
        try:
            proc = subprocess.run(
                [self.executable, "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
            line = (proc.stdout or proc.stderr or "").splitlines()
            return line[0].strip() if line else None
        except (OSError, subprocess.SubprocessError):
            return None

    def metadata(self) -> dict:
        return {
            "provider": "tesseract_cli",
            "engine_version": self._version(),
            "languages": self.languages,
            "psm": self.psm,
            "method": "ocr_tesseract_cli",
        }

    def extract_image(self, image_bytes: bytes, *, page_number: int) -> list[dict]:
        if not self.is_available():
            raise RuntimeError("Tesseract executable is not available")
        with tempfile.TemporaryDirectory() as td:
            image_path = Path(td) / f"page-{page_number}.png"
            image_path.write_bytes(image_bytes)
            proc = subprocess.run(
                [
                    self.executable,
                    str(image_path),
                    "stdout",
                    "-l",
                    self.languages,
                    "--psm",
                    str(self.psm),
                    "tsv",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
            )
            if proc.returncode != 0:
                raise RuntimeError(
                    "Tesseract OCR failed: " + (proc.stderr or proc.stdout or "unknown error").strip()
                )
            return parse_tesseract_tsv(proc.stdout)
