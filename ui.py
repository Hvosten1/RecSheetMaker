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

        self.create_main_tab()
        self.create_edit_tab()
        self.create_directory_tab()  # Вкладка "Справочник рекомендаций"

    def refresh_disease_checkboxes(self):
        """Обновляет список заболеваний"""
        recommendations = load_recommendations()
        if hasattr(self, "disease_frame"):  # **Проверяем, существует ли этот элемент**
            for widget in self.disease_frame.winfo_children():
                widget.destroy()

            for disease in recommendations.keys():
                var = ctk.BooleanVar()
                chk = ctk.CTkCheckBox(self.disease_frame, text=disease, variable=var, font=("Inter", 14))
                chk.pack(anchor="w", padx=10, pady=2)
                self.disease_vars[disease] = var

    def refresh_disease_list(self):
        """Обновляет список болезней в справочнике"""
        recommendations = load_recommendations()
        self.disease_list.configure(values=list(recommendations.keys()))

    def confirm_delete_disease(self):
        """Подтверждение удаления болезни"""
        disease = self.disease_list.get()
        if not disease:
            CTkMessagebox(title="Ошибка", message="Выберите болезнь для удаления!", icon="cancel")
            return

        result = CTkMessagebox(title="Подтверждение", message=f"Удалить '{disease}'?", icon="warning",
                               option_1="Отмена", option_2="Удалить")
        if result.get() == "Удалить":
            self.delete_disease(disease)

    def delete_disease(self, disease):
        """Удаляет болезнь из JSON"""
        recommendations = load_recommendations()
        if disease in recommendations:
            del recommendations[disease]

        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(recommendations, f, ensure_ascii=False, indent=4)

        self.refresh_disease_list()
        self.recommendation_text.configure(state="normal")
        self.recommendation_text.delete("1.0", "end")
        self.recommendation_text.configure(state="disabled")

        CTkMessagebox(title="Готово", message=f"Болезнь '{disease}' удалена!", icon="check")

    def display_recommendation(self, disease):
        """Отображает рекомендацию для выбранной болезни"""
        recommendations = load_recommendations()
        self.recommendation_text.configure(state="normal")
        self.recommendation_text.delete("1.0", "end")
        self.recommendation_text.insert("1.0", recommendations.get(disease, "Нет данных"))
        self.recommendation_text.configure(state="disabled")  # Заблокировать ввод

    def create_main_tab(self):
        """Вкладка для создания рекомендаций"""
        tab_main = self.tabview.add("🩺 Создать рекомендации")

        frame = ctk.CTkFrame(tab_main, corner_radius=20, fg_color="white")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Имя пациента:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)
        self.entry_name = ctk.CTkEntry(frame, width=400, corner_radius=12, font=("Inter", 14))
        self.entry_name.pack(pady=5)

        ctk.CTkLabel(frame, text="Выберите заболевания:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)

        self.disease_vars = {}
        self.disease_frame = ctk.CTkScrollableFrame(frame, width=400, height=200, corner_radius=12, fg_color="#F5F5F5")
        self.disease_frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.refresh_disease_checkboxes()

        self.btn_generate = ctk.CTkButton(frame, text="📄 Создать рекомендации", command=self.generate_recommendations, corner_radius=15, font=("Montserrat", 14))
        self.btn_generate.pack(pady=10)

    def create_edit_tab(self):
        """Вкладка для добавления новых болезней"""
        tab_edit = self.tabview.add("➕ Добавить рекомендации")

        frame = ctk.CTkFrame(tab_edit, corner_radius=20, fg_color="white")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Название болезни:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)
        self.entry_disease = ctk.CTkEntry(frame, width=400, corner_radius=12, font=("Inter", 14))
        self.entry_disease.pack(pady=5)

        ctk.CTkLabel(frame, text="Рекомендация:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)
        self.entry_recommendation = ctk.CTkTextbox(frame, width=400, height=100, corner_radius=12, font=("Inter", 14))
        self.entry_recommendation.pack(pady=5)

        self.btn_add = ctk.CTkButton(frame, text="✅ Добавить", command=self.add_recommendation, corner_radius=15,
                                     font=("Montserrat", 14))
        self.btn_add.pack(pady=10)

    def add_recommendation(self):
        """Добавляет болезнь и её рекомендацию в JSON"""
        disease = self.entry_disease.get().strip()
        recommendation = self.entry_recommendation.get("1.0", "end").strip()
        if not disease or not recommendation:
            CTkMessagebox(title="Ошибка", message="Введите название болезни и рекомендацию!", icon="cancel")
            return

        self.logic.add_recommendation(disease, recommendation)
        self.refresh_disease_checkboxes()
        self.refresh_disease_list()

        CTkMessagebox(title="Готово", message=f'Рекомендация для "{disease}" добавлена!', icon="check")

        self.entry_disease.delete(0, "end")
        self.entry_recommendation.delete("1.0", "end")

    def generate_recommendations(self):
        """Генерация файла рекомендаций"""
        name = self.entry_name.get().strip()
        if not name:
            CTkMessagebox(title="Ошибка", message="Введите имя пациента!", icon="cancel")
            return

        selected_diseases = [d for d, var in self.disease_vars.items() if var.get()]
        if not selected_diseases:
            CTkMessagebox(title="Ошибка", message="Выберите хотя бы одно заболевание!", icon="warning")
            return

        file_path = self.logic.generate_recommendations(name, selected_diseases)

        # Показываем уведомление
        CTkMessagebox(title="Готово", message=f"Рекомендации сохранены:\n{file_path}", icon="info")

    def enable_editing(self):
        """Разблокирует поле для редактирования"""
        self.recommendation_text.configure(state="normal")
        self.btn_save.configure(state="normal")  # Разблокировать кнопку "Сохранить"

    def save_edited_recommendation(self):
        """Сохраняет отредактированную рекомендацию"""
        disease = self.disease_list.get()
        if not disease:
            CTkMessagebox(title="Ошибка", message="Выберите болезнь для редактирования!", icon="cancel")
            return

        new_text = self.recommendation_text.get("1.0", "end").strip()
        if not new_text:
            CTkMessagebox(title="Ошибка", message="Рекомендация не может быть пустой!", icon="cancel")
            return

        recommendations = load_recommendations()
        recommendations[disease] = new_text

        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(recommendations, f, ensure_ascii=False, indent=4)

        self.recommendation_text.configure(state="disabled")
        self.btn_save.configure(state="disabled")  # Заблокировать кнопку "Сохранить"

        CTkMessagebox(title="Готово", message=f'Рекомендация для "{disease}" обновлена!', icon="check")

    def create_directory_tab(self):
        """Вкладка 'Справочник рекомендаций'"""
        tab_directory = self.tabview.add("📚 Справочник рекомендаций")

        frame = ctk.CTkFrame(tab_directory, corner_radius=20, fg_color="white")
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Выберите болезнь:", font=("Montserrat", 16, "bold"), text_color="black").pack(pady=5)

        # Комбобокс, заблокированный для ввода
        self.disease_list = ctk.CTkComboBox(frame, width=400, values=[], command=self.display_recommendation,
                                            state="readonly")
        self.disease_list.pack(pady=5)

        self.recommendation_text = ctk.CTkTextbox(frame, width=400, height=100, corner_radius=12, font=("Inter", 14))
        self.recommendation_text.pack(pady=5)
        self.recommendation_text.configure(state="disabled")

        self.btn_edit = ctk.CTkButton(frame, text="✏ Редактировать", command=self.enable_editing, fg_color="blue",
                                      corner_radius=15, font=("Montserrat", 14))
        self.btn_edit.pack(pady=5)

        self.btn_save = ctk.CTkButton(frame, text="💾 Сохранить", command=self.save_edited_recommendation,
                                      fg_color="green",
                                      corner_radius=15, font=("Montserrat", 14))
        self.btn_save.pack(pady=5)
        self.btn_save.configure(state="disabled")  # Заблокируем кнопку "Сохранить" до редактирования

        self.btn_delete = ctk.CTkButton(frame, text="🗑 Удалить болезнь", command=self.confirm_delete_disease,
                                        fg_color="red", corner_radius=15, font=("Montserrat", 14))
        self.btn_delete.pack(pady=10)

        self.refresh_disease_list()

