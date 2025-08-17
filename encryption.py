import os
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_key(password: str, salt: bytes):
    """Generate a 256-bit AES key from a password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())

def encrypt_file(input_file, output_file, password):
    """Encrypt a file using AES-256-GCM."""
    salt = os.urandom(16)  # Generate random salt
    nonce = os.urandom(12)  # Generate random nonce

    key = generate_key(password, salt)  # Derive key from password

    with open(input_file, "rb") as f:
        plaintext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Store the encrypted data along with metadata
    data = {
        "salt": urlsafe_b64encode(salt).decode(),
        "nonce": urlsafe_b64encode(nonce).decode(),
        "tag": urlsafe_b64encode(encryptor.tag).decode(),
        "ciphertext": urlsafe_b64encode(ciphertext).decode(),
    }

    with open(output_file, "w") as f:
        json.dump(data, f)

    print(f"File encrypted successfully: {output_file}")



