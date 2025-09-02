# Cloud Honeypot – Attack Telemetry → MITRE ATT&CK Mapping 
Projet de cybersécurité : déploiement d’un honeypot SSH dans le cloud, collecte de logs d’attaques réelles, et mappage automatique aux techniques MITRE ATT&CK avec visualisation (heatmap).

## Introduction

Les attaques sur les serveurs exposés en cloud (AWS, GCP, Azure) sont quotidiennes.  
Ce projet met en place un **honeypot SSH (Cowrie)** déployé dans une VM EC2 AWS afin de :  

-  **Collecter** des attaques réelles (tentatives de brute force, commandes malicieuses, transferts de fichiers malwares, etc.)  
-  **Mapper** ces événements aux techniques **MITRE ATT&CK** (framework utilisé par les entreprises FAANG et SOCs)  
-  **Visualiser** les attaques sous forme de heatmap MITRE pour comprendre les tactiques utilisées.  





*(Ici tu insères une capture de ton terminal qui montre `tail -f cowrie.log` avec des bots qui se connectent 🔥)*

---

## Installation & Setup (reproductible)

```md
## Installation & Setup

### 1. Lancer une VM Cloud
- AWS EC2 (Ubuntu 22.04, t2.micro)
- Security Group : TCP 22 (SSH) + 2222 (honeypot) ouverts au monde

### 2. Installer Cowrie
```bash
sudo apt update && sudo apt install -y git python3-venv
git clone https://github.com/cowrie/cowrie
cd cowrie
python3 -m venv cowrie-env
source cowrie-env/bin/activate
pip install -r requirements.txt

```
## Lancer Cowrie

```md
bin/cowrie start
tail -f var/log/cowrie/cowrie.log
```

## Lancer le Mapper MITRE

```md
python heatmap_mitre.py
```
