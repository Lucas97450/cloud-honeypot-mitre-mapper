# Cloud Honeypot – Attack Telemetry → MITRE ATT&CK Mapping 
Projet de cybersécurité : déploiement d’un honeypot SSH dans le cloud, collecte de logs d’attaques réelles, et mappage automatique aux techniques MITRE ATT&CK avec visualisation (heatmap).

## Introduction

Les attaques sur les serveurs exposés en cloud (AWS, GCP, Azure) sont quotidiennes.  
Ce projet met en place un **honeypot SSH (Cowrie)** déployé dans une VM EC2 AWS afin de :  

-  **Collecter** des attaques réelles (tentatives de brute force, commandes malicieuses, transferts de fichiers malwares, etc.)  
-  **Mapper** ces événements aux techniques **MITRE ATT&CK** (framework utilisé par les entreprises FAANG et SOCs)  
-  **Visualiser** les attaques sous forme de heatmap MITRE pour comprendre les tactiques utilisées.  

<img width="715" height="893" alt="Capture d’écran, le 2025-09-02 à 17 44 57" src="https://github.com/user-attachments/assets/b066077b-6c69-4173-b617-c3b8c49ecefc" />

---

## Installation & Setup

```md

# Lancer une VM Cloud
- AWS EC2 (Ubuntu 22.04, t2.micro)
- Security Group : TCP 22 (SSH) + 2222 (honeypot) ouverts au monde

# Installer Cowrie
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
Un fichier mitre_matrix.png est généré automatiquement.

## MITRE ATT&CK – Mapping des attaques observées

Le projet s’appuie sur le framework **MITRE ATT&CK**, référence mondiale pour décrire les tactiques et techniques utilisées par les attaquants.  
Chaque événement capté par **Cowrie** est analysé et, lorsqu’il correspond, **mappé automatiquement** à une technique MITRE (Txxxx).

### Techniques observées dans mes logs
- **T1110 – Brute Force** → Tentatives de login massives avec `root` / `admin`  
- **T1059 – Command-Line Interface** → Exécution de commandes malicieuses (`wget`, `curl`, `echo`)  
- **T1105 – Ingress Tool Transfer** → Téléchargement de malwares via `wget http://...`  
- **T1105 – Application Layer Protocol → Détection de versions SSH utilisées par les bots (fingerprint SSH-2.0-Go, SSH-2.0-libssh, etc.).
- **Reconnaissance – SSH connection attempt → Connexions automatiques depuis des IPs multiples (scanners/IoT bots).

<img width="688" height="835" alt="Capture d’écran, le 2025-09-02 à 17 36 14" src="https://github.com/user-attachments/assets/59f4dddb-bdfb-4363-a163-ba853297d71e" />

### Limites de la couverture
Cowrie est un honeypot **spécialisé SSH/Telnet** → il n’émule pas tous les comportements possibles d’un attaquant.  
Certaines **tactiques MITRE (Exfiltration, Lateral Movement, Impact, etc.)** ne seront pas visibles ici.  

L’objectif n’est donc pas de **couvrir 100% de la matrice MITRE**, mais de :  
1. **Capturer des comportements réels** (bots, brute force, commandes malveillantes)  
2. **Montrer une démarche de Threat Intelligence** : logs → mapping → analyse  
3. **Démontrer ma capacité à travailler avec MITRE ATT&CK** comme le font les SOCs et équipes de détection en entreprise.
