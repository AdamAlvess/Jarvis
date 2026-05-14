import customtkinter as ctk
from tkinter import filedialog
from gui.theme import JARVISTheme
import keyboard

class ConfigEditorWindow(ctk.CTkToplevel):
    def __init__(self, parent_window, mode_to_edit=None, is_new=True):
        super().__init__(parent_window)
        
        self.parent_window = parent_window
        self.mode_name = mode_to_edit
        self.is_new = is_new
        
        # Titre de la fenêtre en fonction du mode (Nouveau ou Édition)
        if self.is_new:
            self.title("J.A.R.V.I.S. - Créer un Nouveau Mode")
            self.mode_data = {"hotkey": "", "actions": []}
        else:
            self.title(f"J.A.R.V.I.S. - Éditer le Mode '{self.mode_name}'")
            self.mode_data = parent_window.modes_config[self.mode_name].copy()
            self.mode_data["actions"] = [action.copy() for action in self.mode_data["actions"]]

        self.geometry("600x600")
        JARVISTheme.apply_to_app(self)
        self.transient(parent_window) 
        
        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) 
        
        # 1. En-tête : Nom et Raccourci
        header_frame = ctk.CTkFrame(self, fg_color=JARVISTheme.FRAME_BG_COLOR, corner_radius=12)
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header_frame, text="Nom du Mode", font=(JARVISTheme.FONT_FAMILY, 13)).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        self.name_entry = ctk.CTkEntry(header_frame, placeholder_text="Ex: Mode Travail", text_color=JARVISTheme.TEXT_COLOR)
        self.name_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        if not self.is_new:
            self.name_entry.insert(0, self.mode_name)
        
        ctk.CTkLabel(header_frame, text="Raccourci (Terminer avec une lettre, chiffre ou Bouton fonction)", font=(JARVISTheme.FONT_FAMILY, 13)).grid(row=2, column=0, padx=15, pady=(0, 5), sticky="w")
        self.hotkey_entry = ctk.CTkEntry(header_frame, placeholder_text="ex: f1", text_color=JARVISTheme.TEXT_COLOR)
        self.hotkey_entry.grid(row=3, column=0, padx=15, pady=(0, 15), sticky="ew")
        if self.mode_data["hotkey"]:
            self.hotkey_entry.insert(0, self.mode_data["hotkey"])
        
        self.record_button = ctk.CTkButton(header_frame, text="Capturer", width=80, 
                                     command=self.record_hotkey, **JARVISTheme.get_button_style())
        self.record_button.grid(row=3, column=1, padx=15, pady=(0, 15))

        # 2. Boutons d'Action
        actions_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_buttons_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.add_exe_button = ctk.CTkButton(actions_buttons_frame, text="+ Ajouter Application (.exe)", **JARVISTheme.get_button_style(), command=self.add_exe_action)
        self.add_exe_button.grid(row=0, column=0, padx=(0, 10), pady=10)
        
        self.add_url_button = ctk.CTkButton(actions_buttons_frame, text="+ Ajouter Lien Web (URL)", **JARVISTheme.get_button_style(), command=self.add_url_action)
        self.add_url_button.grid(row=0, column=1, pady=10)
        
        # 3. Zone Centrale : Liste des Actions (Scrollable)
        self.actions_frame = ctk.CTkScrollableFrame(self, **JARVISTheme.get_frame_style())
        self.actions_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.actions_frame.grid_columnconfigure(0, weight=1)
        
        # 4. Pied de page
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        
        self.save_button = ctk.CTkButton(footer_frame, text="Sauvegarder", **JARVISTheme.get_button_style(), command=self.save_changes)
        self.save_button.grid(row=0, column=0, padx=(0, 10))
        
        self.cancel_button = ctk.CTkButton(footer_frame, text="Annuler", fg_color="#aaaaaa", text_color=JARVISTheme.BG_COLOR, hover_color="#cccccc", font=(JARVISTheme.FONT_FAMILY, 12), command=self.destroy)
        self.cancel_button.grid(row=0, column=1)
        
        # Lancement initial de la liste
        self.refresh_actions_list()

    # --- LES FONCTIONS DE LOGIQUE ---

    def refresh_actions_list(self):
        """C'ÉTAIT CETTE FONCTION QUI MANQUAIT ! Elle reconstruit l'affichage des actions."""
        # On vide la liste actuelle
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
            
        # On recrée chaque ligne d'action
        for i, action in enumerate(self.mode_data["actions"]):
            self.create_action_item_frame(action, i)

    def record_hotkey(self):
        """Capture n'importe quelle combinaison, même sans lettre (ex: Ctrl+Alt)."""
        self.record_button.configure(text="Écoute...", fg_color="#ff9800")
        self.update()

        keys_pressed = set()
        
        def on_key_event(event):
            if event.event_type == "down":
                keys_pressed.add(event.name)
            return False

        # On commence l'écoute
        handler = keyboard.hook(on_key_event)
        while not keys_pressed:
            self.update()
        
        # Attend que toutes les touches soient relâchées
        while any(keyboard.is_pressed(k) for k in keys_pressed):
            self.update()

        keyboard.unhook(handler)

        # Nettoyage et formatage du raccourci
        # On trie pour avoir un ordre cohérent (ctrl+alt au lieu de alt+ctrl)
        ordered_keys = sorted(list(keys_pressed))
        final_hotkey = "+".join(ordered_keys)
        
        self.hotkey_entry.delete(0, 'end')
        self.hotkey_entry.insert(0, final_hotkey)
        
        self.record_button.configure(text="Capturer", **JARVISTheme.get_button_style())
        print(f"J.A.R.V.I.S. : Raccourci capturé : {final_hotkey}")

    def create_action_item_frame(self, action, index):
        item_frame = ctk.CTkFrame(self.actions_frame, fg_color=JARVISTheme.BG_COLOR, corner_radius=8)
        item_frame.grid(row=index, column=0, padx=10, pady=8, sticky="ew")
        item_frame.grid_columnconfigure(0, weight=1)
        
        icon = "💻" if action["type"] == "exe" else "🌐"
        path_label = ctk.CTkLabel(item_frame, text=f"{icon}  {action['path']}", font=(JARVISTheme.FONT_FAMILY, 12), text_color=JARVISTheme.TEXT_COLOR, wraplength=350, justify="left")
        path_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        delete_btn = ctk.CTkButton(item_frame, text="🗑️", width=30, height=30, **JARVISTheme.get_danger_button_style(), command=lambda idx=index: self.delete_action(idx))
        delete_btn.grid(row=0, column=1, padx=10, pady=10)

    def add_exe_action(self):
        file_path = filedialog.askopenfilename(title="Choisir une application", filetypes=[("Executables", "*.exe"), ("All", "*.*")])
        if file_path:
            clean_path = file_path.replace("/", "\\")
            self.mode_data["actions"].append({"type": "exe", "path": clean_path})
            self.refresh_actions_list()

    def add_url_action(self):
        dialog = ctk.CTkInputDialog(text="Collez l'URL (ex: https://google.com) :", title="Ajouter Lien")
        url = dialog.get_input()
        if url:
            if not url.startswith("http"): url = "https://" + url
            self.mode_data["actions"].append({"type": "url", "path": url})
            self.refresh_actions_list()

    def delete_action(self, index):
        del self.mode_data["actions"][index]
        self.refresh_actions_list()

    def save_changes(self):
        new_name = self.name_entry.get().strip()
        if not new_name: return
        
        self.mode_data["hotkey"] = self.hotkey_entry.get().strip()
        
        if not self.is_new and new_name != self.mode_name:
            del self.parent_window.modes_config[self.mode_name]
            
        self.parent_window.modes_config[new_name] = self.mode_data
        self.parent_window.save_config()
        self.parent_window.refresh_modes_list()
        self.destroy()