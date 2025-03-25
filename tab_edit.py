import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import json
import os
import tab_directory

JSON_FILE = "recommendations.json"

def load_recommendations():
    """Загружает рекомендации из JSON-файла"""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def create_edit_tab(app):
    """Вкладка для добавления новых болезней"""
    tab_edit = app.tabview.add("➕ Добавить рекомендации")

    frame = ctk.CTkFrame(tab_edit, corner_radius=20, fg_color="white")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="Название болезни:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)
    app.entry_disease = ctk.CTkEntry(frame, width=400, corner_radius=12, font=("Inter", 14))
    app.entry_disease.pack(pady=5)

    ctk.CTkLabel(frame, text="Рекомендация:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)
    app.entry_recommendation = ctk.CTkTextbox(frame, width=400, height=100, corner_radius=12, font=("Inter", 14))
    app.entry_recommendation.pack(pady=5)

    app.btn_add = ctk.CTkButton(frame, text="✅ Добавить", command=lambda: add_recommendation(app), corner_radius=15,
                                 font=("Montserrat", 14))
    app.btn_add.pack(pady=10)

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


def add_recommendation(app):
    """Добавляет болезнь и её рекомендацию в JSON"""
    disease = app.entry_disease.get().strip()
    recommendation = app.entry_recommendation.get("1.0", "end").strip()
    if not disease or not recommendation:
        CTkMessagebox(title="Ошибка", message="Введите название болезни и рекомендацию!", icon="cancel")
        return

    app.logic.add_recommendation(disease, recommendation)
    refresh_disease_checkboxes(app)
    tab_directory.refresh_disease_list(app)

    CTkMessagebox(title="Готово", message=f'Рекомендация для "{disease}" добавлена!', icon="check")

    app.entry_disease.delete(0, "end")
    app.entry_recommendation.delete("1.0", "end")

