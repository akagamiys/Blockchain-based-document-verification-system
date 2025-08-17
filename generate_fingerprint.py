import hashlib

def generate_blake2b_fingerprint(file_path):
    """Generate a secure hash fingerprint of a file using BLAKE2b (256-bit)."""
    hasher = hashlib.blake2b(digest_size=32)  # 256-bit hash output
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):  # Read file in chunks
            hasher.update(chunk)
    return hasher.hexdigest()

# Example Usage
file_path = r"requirements.txt"  # Change this to your file
fingerprint = generate_blake2b_fingerprint(file_path)
print(f"Document Fingerprint (BLAKE2b-256): {fingerprint}")
