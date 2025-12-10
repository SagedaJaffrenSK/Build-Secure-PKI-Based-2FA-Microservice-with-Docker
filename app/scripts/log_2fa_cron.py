#!/usr/bin/env python3
import sys
import os

# Add /app/app to Python path so imports work anywhere
sys.path.insert(0, "/app/app")

import datetime
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
    with open(LOG_FILE, "w") as f:
        f.write(f"{timestamp} - 2FA Code: {code}\n")

if __name__ == "__main__":
    main()
