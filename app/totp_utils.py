import hmac
import hashlib
import time
import struct

def generate_totp_code(hex_seed, interval=30, digits=6):
    """
    Generate a TOTP code from a hex seed.
    """
    key = bytes.fromhex(hex_seed)
    counter = int(time.time() // interval)
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[-1] & 0x0F
    code = (struct.unpack(">I", h[o:o+4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return f"{code:0{digits}}"
