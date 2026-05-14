import keyboard
import functools
from core.action_runner import ActionRunner

class HotkeyManager:
    def __init__(self, modes_config):
        self.modes_config = modes_config
        self.registered_hotkeys = {}

    def register_all_hotkeys(self):
        """Enregistre tous les raccourcis clavier définis dans la configuration."""
        # Supprime tous les raccourcis existants avant de réenregistrer
        keyboard.unhook_all()
        self.registered_hotkeys = {}
        
        print("J.A.R.V.I.S. : Enregistrement des raccourcis clavier...")
        
        for mode_name, mode_data in self.modes_config.items():
            hotkey = mode_data.get("hotkey")
            actions = mode_data.get("actions", [])
            
            if hotkey:
                # keyboard.add_hotkey nécessite une fonction à appeler.
                # Nous utilisons functools.partial pour passer les actions à la fonction de rappel.
                action_callback = functools.partial(self.execute_mode_actions, mode_name, actions)
                
                try:
                    # Change suppress=True en suppress=False
                    keyboard.add_hotkey(hotkey, action_callback, suppress=False) # suppress=True pour ne pas propager la touche
                    self.registered_hotkeys[hotkey] = mode_name
                    print(f"  -> Raccourci '{hotkey}' enregistré pour le mode '{mode_name}'")
                except ValueError as e:
                    print(f"J.A.R.V.I.S. : Raccourci invalide '{hotkey}' pour '{mode_name}' : {e}")

    def execute_mode_actions(self, mode_name, actions):
        """Exécute toutes les actions associées à un mode donné."""
        print(f"J.A.R.V.I.S. : Activation du mode '{mode_name}' par raccourci.")
        for action in actions:
            ActionRunner.run_action(action["type"], action["path"])

    def wait_for_hotkeys(self):
        """Maintient le programme en vie pour écouter les raccourcis."""
        # keyboard.wait() est une fonction bloquante qui attend qu'un raccourci soit pressé.
        # Idéal pour la version "runner" de ton app en arrière-plan.
        print("J.A.R.V.I.S. : En attente de vos raccourcis... (Ctrl+C pour quitter)")
        keyboard.wait()