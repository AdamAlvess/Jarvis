import customtkinter as ctk
import json
import os
from gui.theme import JARVISTheme
from gui.config_editor import ConfigEditorWindow
from core.hotkey_manager import HotkeyManager
from core.updater import JarvisUpdater

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.title("J.A.R.V.I.S. - Séquenceur d'Actions")
        self.geometry("800x600")
        JARVISTheme.apply_to_app(self)
        
        # Initialisation des gestionnaires
        self.config_path = os.path.join("configs", "modes.json")
        self.load_config()
        self.hotkey_manager = HotkeyManager(self.modes_config)
        self.hotkey_manager.register_all_hotkeys()
        
        # --- UI LAYOUT ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Panneau latéral de navigation (épuré)
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0, fg_color=JARVISTheme.FRAME_BG_COLOR)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="J.A.R.V.I.S.", font=(JARVISTheme.FONT_FAMILY, 22, "bold"), text_color=JARVISTheme.ACCENT_COLOR)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        self.new_mode_button = ctk.CTkButton(self.sidebar_frame, text="++ Nouveau Mode", **JARVISTheme.get_button_style(), command=self.open_new_mode_editor)
        self.new_mode_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Raccourcis Actifs", font=(JARVISTheme.FONT_FAMILY, 12), text_color="#aaaaaa")
        self.status_label.grid(row=2, column=0, padx=20, pady=(20, 5))
        
        self.status_icon = ctk.CTkLabel(self.sidebar_frame, text="⬤", font=("Arial", 16), text_color=JARVISTheme.ACCENT_COLOR)
        self.status_icon.grid(row=2, column=0, padx=(130, 20), pady=(20, 5), sticky="w")
        
        # Zone principale : Liste des Modes (Scrollable)
        self.modes_frame = ctk.CTkScrollableFrame(self, **JARVISTheme.get_frame_style())
        self.modes_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.modes_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh_modes_list()
        # Planifie la vérification des mises à jour 1 seconde après l'ouverture
        self.after(1000, self.check_startup_updates)

    def check_startup_updates(self):
        """Vérifie en tâche de fond si un patch est disponible."""
        new_version = JarvisUpdater.check_for_updates()
        if new_version:
            self.open_update_prompt(new_version)

    def open_update_prompt(self, version):
        """Ouvre une mini-fenêtre interactive style JARVIS."""
        popup = ctk.CTkToplevel(self)
        popup.title("Mise à jour système")
        popup.geometry("380x180")
        popup.resizable(False, False)
        popup.attributes('-topmost', True) # Reste au premier plan
        
        # Centrer la popup par rapport à la fenêtre principale
        popup.grid_columnconfigure((0, 1), weight=1)
        
        # Message
        msg = f"Mise à jour v{version} disponible.\n\nActiver le protocole de mise à jour ?"
        ctk.CTkLabel(popup, text=msg, font=(JARVISTheme.FONT_FAMILY, 13, "bold"), text_color=JARVISTheme.TEXT_COLOR).grid(row=0, column=0, columnspan=2, padx=20, pady=25)
        
        # Fonction d'installation s'il clique sur Oui
        def install():
            popup.destroy()
            # On change le texte du point lumineux pour montrer le chargement
            self.status_label.configure(text="Mise à jour...")
            self.status_icon.configure(text_color="#ff9800")
            self.update()
            JarvisUpdater.update_software()

        # Bouton OUI
        yes_btn = ctk.CTkButton(popup, text="Installer", **JARVISTheme.get_button_style(), command=install)
        yes_btn.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")
        
        # Bouton NON
        no_btn = ctk.CTkButton(popup, text="Plus tard", fg_color="#333333", text_color="white", hover_color="#444444", command=popup.destroy)
        no_btn.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="ew")

    def load_config(self):
        """Charge la configuration depuis le fichier JSON ou crée une config par défaut."""
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            self.modes_config = {
                "Mode Taff": {
                    "hotkey": "ctrl+alt+w",
                    "actions": [
                        {"type": "exe", "path": "C:\\Windows\\System32\\notepad.exe"},
                        {"type": "url", "path": "https://www.google.com"}
                    ]
                }
            }
            self.save_config()
        else:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.modes_config = json.load(f)

    # Dans gui/main_window.py

    def save_config(self):
        """Sauvegarde la configuration et réactive les raccourcis automatiquement."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.modes_config, f, indent=4, ensure_ascii=False)
        
        # On met à jour la config dans le gestionnaire et on relance l'écoute
        if hasattr(self, 'hotkey_manager'):
            self.hotkey_manager.modes_config = self.modes_config
            self.hotkey_manager.register_all_hotkeys()
            print("J.A.R.V.I.S. : Configuration appliquée automatiquement.")

    def refresh_modes_list(self):
        """Efface et reconstruit la liste des modes affichés."""
        # Supprime tous les widgets enfants du scrollable frame
        for widget in self.modes_frame.winfo_children():
            widget.destroy()
            
        # Reconstruit la liste des modes
        for i, (mode_name, mode_data) in enumerate(self.modes_config.items()):
            self.create_mode_item_frame(mode_name, mode_data, i)

    def create_mode_item_frame(self, mode_name, mode_data, index):
        """Crée un cadre pour un mode individuel dans la liste."""
        item_frame = ctk.CTkFrame(self.modes_frame, fg_color=JARVISTheme.BG_COLOR, corner_radius=10)
        item_frame.grid(row=index, column=0, padx=10, pady=10, sticky="ew")
        item_frame.grid_columnconfigure(0, weight=1)
        
        # Nom du mode
        name_label = ctk.CTkLabel(item_frame, text=mode_name, font=(JARVISTheme.FONT_FAMILY, 16, "bold"), text_color=JARVISTheme.TEXT_COLOR)
        name_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        # Raccourci
        hotkey_label = ctk.CTkLabel(item_frame, text=f"Raccourci : {mode_data.get('hotkey', 'Aucun')}", font=(JARVISTheme.FONT_FAMILY, 13), text_color="#aaaaaa")
        hotkey_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")
        
        # Bouton Éditer
        edit_button = ctk.CTkButton(item_frame, text="Éditer", width=80, **JARVISTheme.get_button_style(), command=lambda mn=mode_name: self.open_mode_editor(mn))
        edit_button.grid(row=0, column=1, rowspan=2, padx=(5, 10), pady=15, sticky="e")
        
        # Bouton Supprimer
        delete_button = ctk.CTkButton(item_frame, text="Supprimer", width=90, **JARVISTheme.get_danger_button_style(), command=lambda mn=mode_name: self.delete_mode(mn))
        delete_button.grid(row=0, column=2, rowspan=2, padx=(0, 15), pady=15, sticky="e")

    def open_new_mode_editor(self):
        """Ouvre l'éditeur de configuration pour créer un nouveau mode."""
        self.editor_window = ConfigEditorWindow(self, mode_to_edit=None, is_new=True)
        self.editor_window.focus()

    def open_mode_editor(self, mode_name):
        """Ouvre l'éditeur de configuration pour éditer un mode existant."""
        self.editor_window = ConfigEditorWindow(self, mode_to_edit=mode_name, is_new=False)
        self.editor_window.focus()

    def delete_mode(self, mode_name):
        """Supprime un mode de la configuration et rafraîchit l'interface."""
        if mode_name in self.modes_config:
            del self.modes_config[mode_name]
            self.save_config()
            self.refresh_modes_list()
            print(f"J.A.R.V.I.S. : Mode '{mode_name}' supprimé.")
            
    def apply_hotkeys(self):
        """Applique les raccourcis clavier actuels."""
        self.status_icon.configure(text_color="#f44336") # Changement de couleur temporaire pour "traitement"
        self.status_icon.update()
        
        self.hotkey_manager.modes_config = self.modes_config
        self.hotkey_manager.register_all_hotkeys()
        
        # Animation simple de statut pour le style
        self.after(500, lambda: self.status_icon.configure(text_color=JARVISTheme.ACCENT_COLOR))
        print("J.A.R.V.I.S. : Raccourcis appliqués et à l'écoute.")