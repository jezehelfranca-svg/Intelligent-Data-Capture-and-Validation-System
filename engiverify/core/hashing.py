"""Hashing utilities used to identify immutable source content."""
from hashlib import sha256
from pathlib import Path

def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()

def sha256_file(path, chunk_size: int = 1024 * 1024) -> str:
    digest = sha256()
    with Path(path).open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()
