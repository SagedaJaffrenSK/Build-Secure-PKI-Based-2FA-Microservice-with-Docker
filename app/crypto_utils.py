from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import base64

# RSA/OAEP-SHA256 decrypt
def rsa_oaep_decrypt(encrypted_b64: str, private_key_pem: bytes) -> str:
    encrypted = base64.b64decode(encrypted_b64)
    priv = serialization.load_pem_private_key(private_key_pem, password=None)
    plaintext = priv.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    seed = plaintext.decode('utf-8').strip()
    # Validate 64-char lowercase hex
    seed = seed.lower()
    if len(seed) != 64 or any(c not in '0123456789abcdef' for c in seed):
        raise ValueError("Decrypted seed invalid format")
    return seed

# RSA-PSS-SHA256 signature
def rsa_pss_sign(message: bytes, private_key_pem: bytes) -> bytes:
    priv = serialization.load_pem_private_key(private_key_pem, password=None)
    signature = priv.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# RSA-OAEP-SHA256 encrypt with public key
def rsa_oaep_encrypt(data: bytes, public_key_pem: bytes) -> bytes:
    pub = serialization.load_pem_public_key(public_key_pem)
    ciphertext = pub.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext
