import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import json
import os
from tab_main import create_main_tab
from tab_edit import create_edit_tab
from tab_directory import create_directory_tab

JSON_FILE = "recommendations.json"

def load_recommendations():
    """Загружает рекомендации из JSON-файла"""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

class RecommendationApp(ctk.CTk):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        self.title("AI Врач - Современный помощник")
        self.geometry("800x600")

        # **Светлая тема**
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # **Светлый фон**
        self.configure(bg="#F5F5F5")

        # Главное окно с вкладками
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        create_main_tab(self)
        create_edit_tab(self)
        create_directory_tab(self)  # Вкладка "Справочник рекомендаций"





