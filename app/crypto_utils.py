# app/scripts/crypto_utils.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from pathlib import Path

def decrypt_signature(sig_b64: str) -> str:
    """
    Decrypt base64-encoded RSA ciphertext using PKCS1_v1_5 and return hex seed.
    """
    data = base64.b64decode(sig_b64)
    key_pem = Path("/app/student_private.pem")
    # If your Dockerfile copied student_private.pem to /app root, this path is correct.
    if not key_pem.exists():
        # fallback to /app/app/scripts/student_private.pem if you stored there
        key_pem = Path("/app/app/scripts/student_private.pem")
    priv = RSA.import_key(key_pem.read_text())
    cipher = PKCS1_v1_5.new(priv)
    decrypted = cipher.decrypt(data, None)
    if decrypted is None:
        raise ValueError("RSA decrypt failed")
    return decrypted.hex()
