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

def refresh_disease_list(app):
    """Обновляет список болезней в справочнике"""
    recommendations = load_recommendations()
    app.disease_list.configure(values=list(recommendations.keys()))


def confirm_delete_disease(app):
    """Подтверждение удаления болезни"""
    disease = app.disease_list.get()
    if not disease:
        CTkMessagebox(title="Ошибка", message="Выберите болезнь для удаления!", icon="cancel")
        return

    result = CTkMessagebox(title="Подтверждение", message=f"Удалить '{disease}'?", icon="warning",
                           option_1="Отмена", option_2="Удалить")
    if result.get() == "Удалить":
        app.delete_disease(disease)


def delete_disease(app, disease):
    """Удаляет болезнь из JSON"""
    recommendations = load_recommendations()
    if disease in recommendations:
        del recommendations[disease]

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(recommendations, f, ensure_ascii=False, indent=4)

    app.refresh_disease_list()
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


def generate_recommendations(app):
    """Генерация файла рекомендаций"""
    name = app.entry_name.get().strip()
    if not name:
        CTkMessagebox(title="Ошибка", message="Введите имя пациента!", icon="cancel")
        return

    selected_diseases = [d for d, var in app.disease_vars.items() if var.get()]
    if not selected_diseases:
        CTkMessagebox(title="Ошибка", message="Выберите хотя бы одно заболевание!", icon="warning")
        return

    file_path = app.logic.generate_recommendations(name, selected_diseases)

    # Показываем уведомление
    CTkMessagebox(title="Готово", message=f"Рекомендации сохранены:\n{file_path}", icon="info")


def enable_editing(app):
    """Разблокирует поле для редактирования"""
    app.recommendation_text.configure(state="normal")
    app.btn_save.configure(state="normal")  # Разблокировать кнопку "Сохранить"


def save_edited_recommendation(app):
    """Сохраняет отредактированную рекомендацию"""
    disease = app.disease_list.get()
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

    # Комбобокс, заблокированный для ввода
    app.disease_list = ctk.CTkComboBox(frame, width=400, values=[],
                                       command=lambda disease: display_recommendation(app, disease),
                                       state="readonly")

    app.disease_list.pack(pady=5)

    app.recommendation_text = ctk.CTkTextbox(frame, width=400, height=100, corner_radius=12, font=("Inter", 14))
    app.recommendation_text.pack(pady=5)
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