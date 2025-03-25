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

def refresh_disease_list(app, search_query=""):
    """Обновляет список болезней в справочнике с учетом поиска"""
    recommendations = load_recommendations()
    sorted_diseases = sorted(recommendations.keys())  # Сортируем по алфавиту

    # Фильтруем по поисковому запросу
    if search_query:
        sorted_diseases = [d for d in sorted_diseases if search_query.lower() in d.lower()]

    # Очистка существующих элементов
    for widget in app.disease_list_frame.winfo_children():
        widget.destroy()

    app.disease_var.set("")  # Сбрасываем выбранную болезнь

    for disease in sorted_diseases:
        radio_btn = ctk.CTkRadioButton(
            app.disease_list_frame,
            text=disease,
            variable=app.disease_var,
            value=disease,
            font=("Inter", 14),
            command=lambda d=disease: display_recommendation(app, d)
        )
        radio_btn.pack(anchor="w", padx=5, pady=2)

def search_diseases(app):
    """Функция поиска при изменении текста"""
    search_query = app.search_entry.get()
    refresh_disease_list(app, search_query)

def confirm_delete_disease(app):
    """Подтверждение удаления болезни"""
    disease = app.disease_var.get()
    if not disease:
        CTkMessagebox(title="Ошибка", message="Выберите болезнь для удаления!", icon="cancel")
        return

    result = CTkMessagebox(title="Подтверждение", message=f"Удалить '{disease}'?", icon="warning",
                           option_1="Отмена", option_2="Удалить")
    if result.get() == "Удалить":
        delete_disease(app, disease)

def delete_disease(app, disease):
    """Удаляет болезнь из JSON"""
    recommendations = load_recommendations()
    if disease in recommendations:
        del recommendations[disease]

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(recommendations, f, ensure_ascii=False, indent=4)

    refresh_disease_list(app)
    app.recommendation_text.configure(state="normal")
    app.recommendation_text.delete("1.0", "end")
    app.recommendation_text.configure(state="disabled")

    CTkMessagebox(title="Готово", message=f"Болезнь '{disease}' удалена!", icon="check")

def display_recommendation(app, disease):
    """Отображает рекомендацию для выбранной болезни"""
    recommendations = load_recommendations()
    app.recommendation_text.configure(state="normal")
    app.recommendation_text.delete("1.0", "end")
    app.recommendation_text.insert("1.0", recommendations.get(disease, "Нет данных"))
    app.recommendation_text.configure(state="disabled")  # Заблокировать ввод

def enable_editing(app):
    """Разблокирует поле для редактирования"""
    app.recommendation_text.configure(state="normal")
    app.btn_save.configure(state="normal")  # Разблокировать кнопку "Сохранить"

def save_edited_recommendation(app):
    """Сохраняет отредактированную рекомендацию"""
    disease = app.disease_var.get()
    if not disease:
        CTkMessagebox(title="Ошибка", message="Выберите болезнь для редактирования!", icon="cancel")
        return

    new_text = app.recommendation_text.get("1.0", "end").strip()
    if not new_text:
        CTkMessagebox(title="Ошибка", message="Рекомендация не может быть пустой!", icon="cancel")
        return

    recommendations = load_recommendations()
    recommendations[disease] = new_text

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(recommendations, f, ensure_ascii=False, indent=4)

    app.recommendation_text.configure(state="disabled")
    app.btn_save.configure(state="disabled")  # Заблокировать кнопку "Сохранить"

    CTkMessagebox(title="Готово", message=f'Рекомендация для "{disease}" обновлена!', icon="check")

def create_directory_tab(app):
    """Вкладка 'Справочник рекомендаций'"""
    tab_directory = app.tabview.add("📚 Справочник рекомендаций")

    frame = ctk.CTkFrame(tab_directory, corner_radius=20, fg_color="white")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="Выберите болезнь:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)

    # Поле поиска
    app.search_entry = ctk.CTkEntry(frame, width=400, placeholder_text="🔍 Поиск болезни...", font=("Inter", 12))
    app.search_entry.pack(pady=5)
    app.search_entry.bind("<KeyRelease>", lambda event: search_diseases(app))  # Обновлять при вводе

    # Список болезней с прокруткой
    app.disease_var = ctk.StringVar()

    app.scrollable_frame = ctk.CTkScrollableFrame(frame, width=800, height=200, corner_radius=12, fg_color="#F8F9FA")
    app.scrollable_frame.pack(pady=5, padx=5, expand=True)

    app.disease_list_frame = ctk.CTkFrame(app.scrollable_frame, fg_color="transparent")
    app.disease_list_frame.pack(fill="both", expand=True)

    refresh_disease_list(app)

    app.recommendation_text = ctk.CTkTextbox(frame, width=800, height=250, corner_radius=12, font=("Inter", 14))
    app.recommendation_text.pack(pady=5, padx=5, expand=True)
    app.recommendation_text.configure(state="disabled")

    app.btn_edit = ctk.CTkButton(frame, text="✏ Редактировать", command=lambda: enable_editing(app), fg_color="blue",
                                 corner_radius=15, font=("Montserrat", 14))
    app.btn_edit.pack(pady=5)

    app.btn_save = ctk.CTkButton(frame, text="💾 Сохранить", command=lambda: save_edited_recommendation(app),
                                 fg_color="green",
                                 corner_radius=15, font=("Montserrat", 14))
    app.btn_save.pack(pady=5)
    app.btn_save.configure(state="disabled")  # Заблокируем кнопку "Сохранить" до редактирования

    app.btn_delete = ctk.CTkButton(frame, text="🗑 Удалить болезнь", command=lambda: confirm_delete_disease(app),
                                   fg_color="red", corner_radius=15, font=("Montserrat", 14))
    app.btn_delete.pack(pady=10)

    refresh_disease_list(app)
