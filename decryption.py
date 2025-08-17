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

def decrypt_file(input_file, output_file, password):
    """Decrypt a file encrypted using AES-256-GCM."""
    with open(input_file, "r") as f:
        data = json.load(f)

    # Decode metadata
    salt = urlsafe_b64decode(data["salt"])
    nonce = urlsafe_b64decode(data["nonce"])
    tag = urlsafe_b64decode(data["tag"])
    ciphertext = urlsafe_b64decode(data["ciphertext"])

    key = generate_key(password, salt)  # Recreate key from password

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"File decrypted successfully: {output_file}")


