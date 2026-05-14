import customtkinter as ctk

# Palette de couleurs "hi-tech" épurée
class JARVISTheme:
    BG_COLOR = "#121212"        # Fond très sombre
    FRAME_BG_COLOR = "#1e1e1e"  # Fond des cadres gris foncé
    TEXT_COLOR = "#e0e0e0"     # Texte gris clair
    ACCENT_COLOR = "#00bcd4"  # Cyan pour les accents (comme le HUD de Tony Stark)
    ACCENT_COLOR_HOVER = "#00e5ff" # Cyan plus clair pour le survol
    DANGER_COLOR = "#9a3939"  # Rouge pour la suppression
    
    FONT_FAMILY = "Segoe UI" # Une police épurée et moderne

    @classmethod
    def apply_to_app(cls, app):
        ctk.set_appearance_mode("dark")  # Mode sombre
        ctk.set_default_color_theme("dark-blue")  # Base de thème sombre

    @classmethod
    def get_button_style(cls):
        return {
            "fg_color": cls.ACCENT_COLOR,
            "hover_color": cls.ACCENT_COLOR_HOVER,
            "text_color": cls.BG_COLOR,
            "font": (cls.FONT_FAMILY, 13, "bold"),
            "corner_radius": 8
        }
    
    @classmethod
    def get_danger_button_style(cls):
        return {
            "fg_color": cls.DANGER_COLOR,
            "hover_color": "#9a3939",
            "text_color": "white",
            "font": (cls.FONT_FAMILY, 12, "bold"),
            "corner_radius": 8
        }
    
    @classmethod
    def get_frame_style(cls):
        return {
            "fg_color": cls.FRAME_BG_COLOR,
            "corner_radius": 12,
            "border_width": 1,
            "border_color": "#2c2c2c"
        }