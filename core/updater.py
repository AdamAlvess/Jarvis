import os
import sys
import subprocess
import requests

CURRENT_VERSION = "1.0.0"  # Version locale de l'exe actuel

# ⚠️ REMPLACE PAR TES INFOS REELLES GITHUB
GITHUB_USER = "AdamAlvess"
GITHUB_REPO = "Jarvis"

VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/configs/version.json"
EXE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/dist/JARVIS.exe"

class JarvisUpdater:
    @staticmethod
    def check_for_updates():
        """Vérifie uniquement si une mise à jour existe (renvoie la version ou None)."""
        try:
            response = requests.get(VERSION_URL, timeout=5)
            if response.status_code == 200:
                online_data = response.json()
                online_version = online_data.get("version", CURRENT_VERSION)
                
                if online_version != CURRENT_VERSION:
                    return online_version
        except Exception as e:
            print(f"J.A.R.V.I.S. : Impossible de vérifier les mises à jour : {e}")
        return None

    @staticmethod
    def update_software():
        """Déclenche le téléchargement et l'installation de la mise à jour."""
        try:
            response = requests.get(EXE_URL, stream=True, timeout=30)
            if response.status_code == 200:
                next_exe = "JARVIS_next.exe"
                with open(next_exe, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                JarvisUpdater.trigger_upgrade_script()
        except Exception as e:
            print(f"J.A.R.V.I.S. : Erreur pendant la mise à jour : {e}")

    @staticmethod
    def trigger_upgrade_script():
        """Crée et lance le script de transition invisible."""
        current_exe = sys.argv[0]
        if not current_exe.endswith(".exe"):
            print("J.A.R.V.I.S. : Mode Dev détecté. Remplacement de l'EXE annulé.")
            return

        bat_content = f"""
        @echo off
        timeout /t 1 /nobreak > nul
        del "{current_exe}"
        rename "JARVIS_next.exe" "JARVIS.exe"
        start "" "JARVIS.exe"
        del "%~f0"
        """
        with open("upgrade.bat", "w") as f:
            f.write(bat_content)
            
        subprocess.Popen(["cmd", "/c", "upgrade.bat"], creationflags=subprocess.CREATE_NO_WINDOW)
        sys.exit()