import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Пути к файлам
JSON_FILE = "recommendations.json"
OUTPUT_FOLDER = "recommendations"

# Проверяем, существует ли JSON-файл, если нет — создаем пустой
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

# Загружаем рекомендации из JSON
def load_recommendations():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Основное окно
root = tk.Tk()
root.title("Помощник врача")
root.geometry("500x400")

# Создаем вкладки
tab_control = ttk.Notebook(root)

# Вкладки
tab_main = ttk.Frame(tab_control)
tab_edit = ttk.Frame(tab_control)

tab_control.add(tab_main, text="Создать рекомендации")
tab_control.add(tab_edit, text="Редактор рекомендаций")
tab_control.pack(expand=1, fill="both")

# ** Вкладка "Создать рекомендации" **

# Поле ввода имени пациента
tk.Label(tab_main, text="Имя пациента:").pack(pady=5)
entry_name = tk.Entry(tab_main, width=40)
entry_name.pack(pady=5)

# Загружаем список болезней
recommendations = load_recommendations()
disease_vars = {}  # Словарь для чекбоксов

tk.Label(tab_main, text="Выберите заболевания:").pack(pady=5)
frame_diseases = tk.Frame(tab_main)
frame_diseases.pack()

# Создаем чекбоксы
for disease in recommendations.keys():
    var = tk.BooleanVar()
    chk = tk.Checkbutton(frame_diseases, text=disease, variable=var)
    chk.pack(anchor="w")
    disease_vars[disease] = var

# Кнопка для генерации файла рекомендаций
btn_generate = tk.Button(tab_main, text="Создать рекомендации", command=lambda: generate_recommendations(entry_name.get(), disease_vars, recommendations))
btn_generate.pack(pady=10)

# ** Вкладка "Редактор рекомендаций" **

tk.Label(tab_edit, text="Название болезни:").pack(pady=5)
entry_disease = tk.Entry(tab_edit, width=40)
entry_disease.pack(pady=5)

tk.Label(tab_edit, text="Рекомендация:").pack(pady=5)
entry_recommendation = tk.Text(tab_edit, width=40, height=5)
entry_recommendation.pack(pady=5)

btn_add = tk.Button(tab_edit, text="Добавить", command=lambda: add_recommendation(entry_disease.get(), entry_recommendation.get("1.0", "end").strip()))
btn_add.pack(pady=10)

# Функции

def generate_recommendations(name, disease_vars, recommendations):
    """Генерирует файл с рекомендациями"""
    if not name.strip():
        messagebox.showerror("Ошибка", "Введите имя пациента!")
        return

    selected_diseases = [d for d, var in disease_vars.items() if var.get()]
    if not selected_diseases:
        messagebox.showerror("Ошибка", "Выберите хотя бы одно заболевание!")
        return

    print("Выбранные болезни:", selected_diseases)
    print("Текущие рекомендации:", recommendations)  # Отладочный вывод

    # Создаем папку, если её нет
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Формируем содержимое файла
    file_content = f"Пациент: {name}\n\nРекомендации:\n"
    for disease in selected_diseases:
        recommendation = recommendations.get(disease, "Нет рекомендаций")  # Безопасный доступ
        file_content += f"- {disease}: {recommendation}\n"

    # Сохраняем файл
    file_path = os.path.join(OUTPUT_FOLDER, f"{name}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)

    messagebox.showinfo("Готово", f"Рекомендации сохранены: {file_path}")


def add_recommendation(disease, recommendation):
    """Добавляет новую болезнь и рекомендацию в JSON"""
    if not disease.strip() or not recommendation.strip():
        messagebox.showerror("Ошибка", "Введите название болезни и рекомендацию!")
        return

    # Загружаем текущие рекомендации
    recommendations = load_recommendations()
    recommendations[disease] = recommendation

    # Сохраняем в файл
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(recommendations, f, ensure_ascii=False, indent=4)

    messagebox.showinfo("Готово", "Рекомендация добавлена!")

    # Очищаем поля ввода
    entry_disease.delete(0, "end")
    entry_recommendation.delete("1.0", "end")

    # Обновляем чекбоксы на первой вкладке
    refresh_disease_checkboxes()

def refresh_disease_checkboxes():
    """Обновляет список чекбоксов после добавления новой болезни"""
    global disease_vars
    recommendations = load_recommendations()

    # Очищаем старые чекбоксы
    for widget in frame_diseases.winfo_children():
        widget.destroy()

    disease_vars = {}
    for disease in recommendations.keys():
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame_diseases, text=disease, variable=var)
        chk.pack(anchor="w")
        disease_vars[disease] = var

# Запускаем интерфейс
root.mainloop()
