"""Safe source-document registration and immutable local storage."""
from datetime import datetime, timezone
import mimetypes
from pathlib import Path
import re
import shutil

from engiverify.core.hashing import sha256_file

_UNSAFE = re.compile(r"[^A-Za-z0-9._()\- ]+")

def safe_filename(name: str) -> str:
    base = Path(str(name)).name.strip()
    base = _UNSAFE.sub("_", base).strip(" .")
    if not base or base in {".", ".."}:
        raise ValueError("Source filename is empty or unsafe")
    return base[:240]

def build_source_manifest(
    path,
    *,
    project_id: str,
    document_type: str,
    document_revision: str,
    source_document_id: str | None = None,
):
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    digest = sha256_file(source)
    media_type = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
    return {
        "source_document_id": source_document_id or f"SRC-{digest[:16]}",
        "project_id": project_id,
        "original_filename": safe_filename(source.name),
        "sha256": digest,
        "size_bytes": source.stat().st_size,
        "media_type": media_type,
        "document_type": document_type,
        "document_revision": str(document_revision),
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }

def store_immutable(source_path, storage_root):
    source = Path(source_path)
    digest = sha256_file(source)
    filename = safe_filename(source.name)
    destination = Path(storage_root) / digest[:2] / digest / filename
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        if sha256_file(destination) != digest:
            raise RuntimeError("Existing immutable destination does not match source hash")
        return destination

    with source.open("rb") as src, destination.open("xb") as dst:
        shutil.copyfileobj(src, dst)
    if sha256_file(destination) != digest:
        destination.unlink(missing_ok=True)
        raise RuntimeError("Immutable copy failed hash verification")
    return destination
