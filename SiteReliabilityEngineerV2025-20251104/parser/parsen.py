#!/usr/bin/env python3
import time
import os
import re
import json
from glob import glob

# Pola log: timestamp service status response_time_ms app_version user_id transaction_id
LOG_RE = re.compile(r'(\S+) (\S+) (\d{3}) (\d+)ms (v[\d\.]+) (user_\d+) (trx_\d+)')

RAW_DIR = "/rawlogs"     # mounted read-only
OUT_DIR = "/parsed"     # mounted writeable
OUT_FILE = os.path.join(OUT_DIR, "parsed.jsonl")

def follow_files(paths):
    """Generator that yields new lines from multiple files (tail -f)."""
    files = []
    for p in paths:
        try:
            f = open(p, "r", encoding="utf-8", errors="ignore")
            # seek to end so we only process new logs (but we also read existing lines once)
            # go to start to parse existing content as well:
            f.seek(0, os.SEEK_SET)
            files.append((p, f))
        except FileNotFoundError:
            continue
    while True:
        any_read = False
        for p, f in files:
            line = f.readline()
            if not line:
                continue
            any_read = True
            yield line
        if not any_read:
            time.sleep(0.5)
            # attempt to detect new files
            current = set(p for p, _ in files)
            for p in glob(os.path.join(RAW_DIR, "*.log")):
                if p not in current:
                    try:
                        nf = open(p, "r", encoding="utf-8", errors="ignore")
                        files.append((p, nf))
                    except Exception:
                        pass

def parse_line(line):
    m = LOG_RE.search(line.strip())
    if not m:
        return None
    ts, service, status, rt, version, user, trx = m.groups()
    obj = {
        "timestamp": ts,
        "service": service,
        "status_code": int(status),
        "response_time_ms": int(rt),
        "app_version": version,
        "user_id": user,
        "transaction_id": trx,
        "raw_line": line.strip()
    }
    return obj

def ensure_out():
    os.makedirs(OUT_DIR, exist_ok=True)
    # create file if not exists
    open(OUT_FILE, "a").close()

def main():
    ensure_out()
    paths = glob(os.path.join(RAW_DIR, "*.log"))
    print("Parser starting. Watching files:", paths)
    with open(OUT_FILE, "a", encoding="utf-8") as out:
        for line in follow_files(paths):
            obj = parse_line(line)
            if obj:
                out.write(json.dumps(obj, ensure_ascii=False) + "\n")
                out.flush()

if __name__ == "__main__":
    main()

