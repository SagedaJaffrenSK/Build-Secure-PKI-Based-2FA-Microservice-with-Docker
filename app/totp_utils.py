# app/scripts/totp_utils.py
import pyotp
import qrcode
from io import BytesIO
import base64

def generate_secret_uri(label="student", issuer="PKI-2FA"):
    secret = pyotp.random_base32()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=label,
        issuer_name=issuer
    )
    return secret, uri

def verify_token(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)
