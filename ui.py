import customtkinter as ctk
import json
import os
import datetime
from tkinter import messagebox

JSON_FILE = "recommendations.json"
OUTPUT_FOLDER = "recommendations"

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
        self.title("Помощник врача")
        self.geometry("700x550")
        ctk.set_appearance_mode("dark")  # Тёмная тема Material
        ctk.set_default_color_theme("green")  # Цветовая схема

        # Главное окно с вкладками
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_main_tab()
        self.create_edit_tab()

    def create_main_tab(self):
        """Вкладка для создания рекомендаций"""
        tab_main = self.tabview.add("Создать рекомендации")

        # Карточка с полупрозрачным эффектом
        frame = ctk.CTkFrame(tab_main, corner_radius=15)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Имя пациента:", font=("Arial", 14, "bold")).pack(pady=5)
        self.entry_name = ctk.CTkEntry(frame, width=400, corner_radius=10)
        self.entry_name.pack(pady=5)

        ctk.CTkLabel(frame, text="Выберите заболевания:", font=("Arial", 14, "bold")).pack(pady=5)

        self.disease_vars = {}
        self.disease_frame = ctk.CTkScrollableFrame(frame, width=400, height=200, corner_radius=10)
        self.disease_frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.refresh_disease_checkboxes()

        self.btn_generate = ctk.CTkButton(frame, text="Создать рекомендации", command=self.generate_recommendations)
        self.btn_generate.pack(pady=10)

    def create_edit_tab(self):
        """Вкладка для добавления новых болезней"""
        tab_edit = self.tabview.add("Редактор рекомендаций")

        frame = ctk.CTkFrame(tab_edit, corner_radius=15)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Название болезни:", font=("Arial", 14, "bold")).pack(pady=5)
        self.entry_disease = ctk.CTkEntry(frame, width=400, corner_radius=10)
        self.entry_disease.pack(pady=5)

        ctk.CTkLabel(frame, text="Рекомендация:", font=("Arial", 14, "bold")).pack(pady=5)
        self.entry_recommendation = ctk.CTkTextbox(frame, width=400, height=100, corner_radius=10)
        self.entry_recommendation.pack(pady=5)

        self.btn_add = ctk.CTkButton(frame, text="Добавить", command=self.add_recommendation)
        self.btn_add.pack(pady=10)

    def refresh_disease_checkboxes(self):
        """Обновляет список заболеваний"""
        for widget in self.disease_frame.winfo_children():
            widget.destroy()

        recommendations = load_recommendations()
        self.disease_vars = {}

        for disease in recommendations.keys():
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(self.disease_frame, text=disease, variable=var)
            chk.pack(anchor="w", padx=10, pady=2)
            self.disease_vars[disease] = var

    def generate_recommendations(self):
        """Генерация файла рекомендаций"""
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите имя пациента!")
            return

        selected_diseases = [d for d, var in self.disease_vars.items() if var.get()]
        if not selected_diseases:
            messagebox.showerror("Ошибка", "Выберите хотя бы одно заболевание!")
            return

        file_path = self.logic.generate_recommendations(name, selected_diseases)

        # Показываем уведомление
        messagebox.showinfo("Готово", f"Рекомендации сохранены:\n{file_path}")

    def add_recommendation(self):
        """Добавляет болезнь в JSON и выводит уведомление"""
        disease = self.entry_disease.get().strip()
        recommendation = self.entry_recommendation.get("1.0", "end").strip()
        if not disease or not recommendation:
            messagebox.showerror("Ошибка", "Введите название болезни и рекомендацию!")
            return

        self.logic.add_recommendation(disease, recommendation)
        self.refresh_disease_checkboxes()

        # Показываем уведомление об успешном добавлении
        messagebox.showinfo("Готово", f'Рекомендация для "{disease}" добавлена!')

        # Очищаем поля ввода
        self.entry_disease.delete(0, "end")
        self.entry_recommendation.delete("1.0", "end")
