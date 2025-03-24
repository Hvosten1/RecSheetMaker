import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import json
import os

JSON_FILE = "recommendations.json"

def load_recommendations():
    """Загружает рекомендации из JSON-файла"""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def create_main_tab(app):
    """Создаёт вкладку для создания рекомендаций"""
    tab_main = app.tabview.add("🩺 Создать рекомендации")

    frame = ctk.CTkFrame(tab_main, corner_radius=20, fg_color="white")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="Имя пациента:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)
    app.entry_name = ctk.CTkEntry(frame, width=400, corner_radius=12, font=("Inter", 14))
    app.entry_name.pack(pady=5)

    ctk.CTkLabel(frame, text="Выберите заболевания:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)

    app.disease_vars = {}
    app.disease_frame = ctk.CTkScrollableFrame(frame, width=400, height=200, corner_radius=12, fg_color="#F5F5F5")
    app.disease_frame.pack(pady=5, padx=10, fill="both", expand=True)

    refresh_disease_checkboxes(app)

    app.btn_generate = ctk.CTkButton(frame, text="📄 Создать рекомендации", command=lambda: generate_recommendations(app), corner_radius=15, font=("Montserrat", 14))
    app.btn_generate.pack(pady=10)

def refresh_disease_checkboxes(app):
    """Обновляет список заболеваний"""
    recommendations = load_recommendations()
    for widget in app.disease_frame.winfo_children():
        widget.destroy()

    for disease in recommendations.keys():
        var = ctk.BooleanVar()
        chk = ctk.CTkCheckBox(app.disease_frame, text=disease, variable=var, font=("Inter", 14))
        chk.pack(anchor="w", padx=10, pady=2)
        app.disease_vars[disease] = var

def generate_recommendations(app):
    """Генерирует рекомендации в файл"""
    name = app.entry_name.get().strip()
    if not name:
        CTkMessagebox(title="Ошибка", message="Введите имя пациента!", icon="cancel")
        return

    selected_diseases = [d for d, var in app.disease_vars.items() if var.get()]
    if not selected_diseases:
        CTkMessagebox(title="Ошибка", message="Выберите хотя бы одно заболевание!", icon="warning")
        return

    file_path = app.logic.generate_recommendations(name, selected_diseases)
    CTkMessagebox(title="Готово", message=f"Рекомендации сохранены:\n{file_path}", icon="info")
