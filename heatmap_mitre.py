#!/usr/bin/env python3
import json
import glob
import os
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

MITRE_MAP = {
    "cowrie.login.failed": ("Credential Access", "T1110 - Brute Force"),
    "cowrie.login.success": ("Credential Access", "T1078 - Valid Accounts"),
    "cowrie.command.input": ("Execution", "T1059 - Command Execution"),
    "cowrie.session.file_download": ("Command and Control", "T1105 - Ingress Tool Transfer"),
    "cowrie.session.file_upload": ("Command and Control", "T1105 - Ingress Tool Transfer"),
    "cowrie.client.version": ("Discovery", "T1049 - System Network Connections Discovery"),
    "cowrie.session.connect": ("Initial Access", "T1021 - Remote Services"),
}

LOG_DIR = "/home/cowrie/cowrie/var/log/cowrie/"
LOG_PATTERN = os.path.join(LOG_DIR, "cowrie.json*")

counts = Counter()

for filepath in glob.glob(LOG_PATTERN):
    with open(filepath) as f:
        for line in f:
            try:
                event = json.loads(line)
                evt = event.get("eventid", "")
                if evt in MITRE_MAP:
                    tactic, technique = MITRE_MAP[evt]
                    counts[(tactic, technique)] += 1
            except json.JSONDecodeError:
                continue

data = {}
for (tactic, technique), value in counts.items():
    if tactic not in data:
        data[tactic] = {}
    data[tactic][technique] = value

df = pd.DataFrame(data).fillna(0).astype(int).T

plt.figure(figsize=(14, 6))
sns.heatmap(df.T, annot=True, fmt="d", cmap="Reds", cbar=True)

plt.title(" MITRE ATT&CK Matrix - Activité Honeypot")
plt.ylabel("Tactics")
plt.xlabel("Techniques Observées")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("mitre_matrix.png")
plt.show()
