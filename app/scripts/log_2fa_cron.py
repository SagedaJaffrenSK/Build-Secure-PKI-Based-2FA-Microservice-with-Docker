#!/usr/bin/env python3
import datetime
import os
from totp_utils import generate_totp_code

SEED_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

def main():
    if not os.path.exists(SEED_FILE):
        print("Seed not found", flush=True)
        return
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()
    code = generate_totp_code(hex_seed)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - 2FA Code: {code}", flush=True)

if __name__ == "__main__":
    main()
