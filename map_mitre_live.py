#!/usr/bin/env python3
import json
import glob
import time
import os

MITRE_MAP = {
    "cowrie.login.failed": "T1110 - Credential Access (Brute Force)",
    "cowrie.login.success": "T1110 - Credential Access (Brute Force)",
    "cowrie.command.input": "T1059 - Execution (Command-Line Interface)",
    "cowrie.session.file_download": "T1105 - Ingress Tool Transfer",
    "cowrie.client.version": "T1071 - Application Layer Protocol",
    "cowrie.session.connect": "Reconnaissance - SSH connection attempt"
}

LOG_DIR = "/home/cowrie/cowrie/var/log/cowrie/"
LOG_PATTERN = os.path.join(LOG_DIR, "cowrie.json*")

def process_line(line):
    """Parse une ligne JSON et affiche si mappable MITRE"""
    try:
        event = json.loads(line)
        evt = event.get("eventid", "")
        src = event.get("src_ip", "unknown")
        ts = event.get("timestamp", "")

        if evt in MITRE_MAP:
            print(f"[{ts}] {src} → {MITRE_MAP[evt]}")
    except json.JSONDecodeError:
        pass

def process_historical():
    """Traite tous les fichiers historiques (cowrie.json + .date)"""
    print("Lecture des anciens logs...\n")
    for filepath in sorted(glob.glob(LOG_PATTERN)):
        with open(filepath) as f:
            for line in f:
                process_line(line)

def follow_live():
    """Mode suivi en direct (tail -f sur cowrie.json)"""
    logfile = os.path.join(LOG_DIR, "cowrie.json")
    print("\n Lecture en direct activé. En attente de nouveaux events...\n")
    with open(logfile) as f:
        f.seek(0, 2)  # va à la fin
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            process_line(line)

if __name__ == "__main__":
    process_historical()
    follow_live()

