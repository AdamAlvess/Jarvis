import os
import sys
import subprocess
import requests

CURRENT_VERSION = "1.0.2"  # La version de ton EXE local

# Infos de ton dépôt
GITHUB_USER = "AdamAlvess"
GITHUB_REPO = "Jarvis"
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"

class JarvisUpdater:
    @staticmethod
    def check_for_updates():
        """Vérifie si une nouvelle Release est disponible sur GitHub via l'API."""
        try:
            # L'API GitHub exige un User-Agent pour accepter la requête
            headers = {"User-Agent": "JARVIS-AutoUpdater"}
            response = requests.get(API_URL, headers=headers, timeout=5)
            
            if response.status_code == 200:
                release_data = response.json()
                # On récupère le nom du tag de la release (ex: "1.0.1" ou "v1.0.1")
                online_version = release_data.get("tag_name", CURRENT_VERSION)
                
                # Nettoyage au cas où tu mets un 'v' devant la version sur GitHub (ex: v1.0.1 -> 1.0.1)
                online_version_clean = online_version.lstrip('v')
                current_version_clean = CURRENT_VERSION.lstrip('v')
                
                if online_version_clean != current_version_clean:
                    print(f"J.A.R.V.I.S. : Nouvelle version détectée : v{online_version_clean}")
                    return online_version
        except Exception as e:
            print(f"J.A.R.V.I.S. : Impossible de vérifier les mises à jour : {e}")
        return None

    @staticmethod
    def update_software():
        """Trouve le fichier JARVIS.exe dans la Release GitHub et le télécharge."""
        try:
            headers = {"User-Agent": "JARVIS-AutoUpdater"}
            response = requests.get(API_URL, headers=headers, timeout=5)
            
            if response.status_code != 200:
                return
                
            release_data = response.json()
            download_url = None
            
            # On parcourt la liste des fichiers attachés (assets) à la release pour trouver JARVIS.exe
            for asset in release_data.get("assets", []):
                if asset.get("name") == "JARVIS.exe":
                    download_url = asset.get("browser_download_url")
                    break
            
            if not download_url:
                print("J.A.R.V.I.S. : Fichier JARVIS.exe introuvable dans la Release GitHub.")
                return
                
            print("J.A.R.V.I.S. : Téléchargement du patch depuis GitHub...")
            exe_response = requests.get(download_url, stream=True, timeout=30)
            
            if exe_response.status_code == 200:
                next_exe = "JARVIS_next.exe"
                with open(next_exe, "wb") as f:
                    for chunk in exe_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                JarvisUpdater.trigger_upgrade_script()
        except Exception as e:
            print(f"J.A.R.V.I.S. : Erreur pendant le téléchargement : {e}")

    @staticmethod
    def trigger_upgrade_script():
        current_exe = sys.argv[0]
        if not current_exe.endswith(".exe"):
            print("J.A.R.V.I.S. : Mode Dev détecté. Remplacement de l'EXE annulé.")
            return

        # On passe le timeout à 3 secondes
        bat_content = f"""
        @echo off
        timeout /t 3 /nobreak > nul
        del "{current_exe}"
        rename "JARVIS_next.exe" "JARVIS.exe"
        start "" "JARVIS.exe"
        del "%~f0"
        """
        with open("upgrade.bat", "w") as f:
            f.write(bat_content)
            
        subprocess.Popen(["cmd", "/c", "upgrade.bat"], creationflags=subprocess.CREATE_NO_WINDOW)
        sys.exit()