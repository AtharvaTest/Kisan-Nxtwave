import hashlib

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_text(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()
