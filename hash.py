import hashlib
from pathlib import Path

def compute_hash(uri: str) -> str:
    """Compute the SHA-256 hash of the content at the given URI."""
    file_path = Path.from_uri(uri)
    print(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File {uri} does not exist.")
    
    with open(file_path, "rb") as f:
        content = f.read()
    
    return hashlib.sha256(content).hexdigest()