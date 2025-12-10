from datetime import datetime
Path = __import__('pathlib').Path
Path("/data").mkdir(parents=True, exist_ok=True)
with open("/data/cron.log","a") as f:
    f.write(datetime.utcnow().isoformat() + "\n")
