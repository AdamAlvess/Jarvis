import subprocess
import webbrowser
import platform

class ActionRunner:
    @staticmethod
    def run_action(action_type, action_path):
        """Exécute une action en fonction de son type (exe ou url)."""
        print(f"J.A.R.V.I.S. : Exécution de l'action {action_type} -> {action_path}")
        
        if action_type == "exe":
            ActionRunner.launch_exe(action_path)
        elif action_type == "url":
            ActionRunner.open_url(action_path)
        else:
            print(f"J.A.R.V.I.S. : Type d'action inconnu : {action_type}")

    @staticmethod
    def launch_exe(exe_path):
        """Lance un fichier exécutable (.exe)."""
        try:
            # Popen permet de lancer le programme en arrière-plan sans bloquer Python
            subprocess.Popen(exe_path)
        except FileNotFoundError:
            print(f"J.A.R.V.I.S. : Fichier .exe introuvable : {exe_path}")
        except Exception as e:
            print(f"J.A.R.V.I.S. : Erreur lors du lancement de l'exe : {e}")

    @staticmethod
    def open_url(url):
        """Ouvre un lien web dans le navigateur par défaut."""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"J.A.R.V.I.S. : Erreur lors de l'ouverture de l'URL : {e}")