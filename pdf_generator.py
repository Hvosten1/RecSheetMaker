from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import simpleSplit
import os
from datetime import datetime
import json

# Путь к файлу со шрифтом
FONT_PATH = "assets/fonts/DejaVuSans.ttf"
JSON_FILE = "recommendations.json"

# Проверяем, существует ли шрифт
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Шрифт '{FONT_PATH}' не найден! Скачайте его и поместите в папку 'assets/fonts/'.")

# Регистрируем шрифт DejaVuSans
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))

def load_recommendations():
    """Загружает рекомендации из JSON-файла"""
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_pdf(patient_name, diseases, recommendations):
    """
    Генерирует PDF-файл с автоматическим переносом строк и блоком 'Общие рекомендации'.
    """
    # Создаём папку для сохранения, если её нет
    output_dir = "recommendations"
    os.makedirs(output_dir, exist_ok=True)

    # Формируем имя файла: ФИО_Дата_Номер.pdf
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"{patient_name}_{date_str}.pdf"
    file_path = os.path.join(output_dir, file_name)

    # Загружаем рекомендации
    all_recommendations = load_recommendations()
    general_recommendation = all_recommendations.get("Общие рекомендации", "Следуйте советам врача и ведите здоровый образ жизни.")

    # Настраиваем PDF
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Используем зарегистрированный шрифт
    c.setFont("DejaVuSans", 16)
    c.drawString(20, height - 50, "Медицинские рекомендации")
    c.setFont("DejaVuSans", 12)
    c.drawString(20, height - 80, "Врач: Хвостунова Татьяна Викторовна")

    # Информация о пациенте
    c.setFont("DejaVuSans", 14)
    c.drawString(20, height - 110, f"Пациент: {patient_name}")

    # Добавляем "Общие рекомендации"
    y_position = height - 140
    c.setFont("DejaVuSans", 12)
    c.drawString(20, y_position, "Общие рекомендации:")
    y_position -= 20

    wrapped_text = simpleSplit(general_recommendation, "DejaVuSans", 11, width - 80)
    c.setFont("DejaVuSans", 11)
    for line in wrapped_text:
        c.drawString(40, y_position, line)
        y_position -= 14

        # Если достигли нижнего края страницы, создаем новую страницу
        if y_position < 50:
            c.showPage()
            c.setFont("DejaVuSans", 11)
            y_position = height - 50

    # Раздел "Назначенные рекомендации"
    y_position -= 20
    c.setFont("DejaVuSans", 12)
    c.drawString(20, y_position, "Назначенные рекомендации:")
    y_position -= 20

    c.setFont("DejaVuSans", 11)
    for disease in diseases:
        recommendation = recommendations.get(disease, "Нет данных")
        full_text = f"• {disease}: {recommendation}"

        wrapped_text = simpleSplit(full_text, "DejaVuSans", 11, width - 80)
        for line in wrapped_text:
            c.drawString(40, y_position, line)
            y_position -= 14

            # Если достигли нижнего края страницы, создаем новую страницу
            if y_position < 50:
                c.showPage()
                c.setFont("DejaVuSans", 11)
                y_position = height - 50

    # Завершаем PDF
    c.save()
    return file_path
