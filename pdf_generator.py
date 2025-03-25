from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import simpleSplit
import os
from datetime import datetime
import json

# Пути к файлам шрифтов
FONT_PATH_REGULAR = "assets/fonts/DejaVuSans.ttf"
FONT_PATH_BOLD = "assets/fonts/DejaVuSans-Bold.ttf"
JSON_FILE = "recommendations.json"

# Проверяем, существуют ли файлы шрифтов
if not os.path.exists(FONT_PATH_REGULAR) or not os.path.exists(FONT_PATH_BOLD):
    raise FileNotFoundError("Один из шрифтов не найден! Скачайте 'DejaVuSans.ttf' и 'DejaVuSans-Bold.ttf' и поместите в 'assets/fonts/'.")

# Регистрируем обычный и жирный шрифт
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH_REGULAR))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", FONT_PATH_BOLD))

def load_recommendations():
    """Загружает рекомендации из JSON-файла"""
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def draw_page_number(c, page_num, width, height):
    """Добавляет номер страницы внизу"""
    c.setFont("DejaVuSans", 10)
    page_text = f"Страница {page_num}"
    c.drawRightString(width - 30, 30, page_text)

def generate_pdf(patient_name, diseases, recommendations):
    """
    Генерирует PDF-файл с автоматическим переносом строк, визуальным разделением рекомендаций и жирными заголовками.
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
    page_num = 1  # Нумерация страниц

    # Используем зарегистрированные шрифты
    c.setFont("DejaVuSans-Bold", 16)
    c.drawString(20, height - 50, "Медицинские рекомендации")
    c.setFont("DejaVuSans", 12)
    c.drawString(20, height - 80, "Врач: Хвостунова Татьяна Викторовна")

    # Информация о пациенте
    c.setFont("DejaVuSans-Bold", 14)
    c.drawString(20, height - 110, f"Пациент: {patient_name}")

    # Добавляем "Общие рекомендации"
    y_position = height - 140
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(20, y_position, "Общие рекомендации:")
    y_position -= 20

    c.setFont("DejaVuSans", 11)
    wrapped_text = simpleSplit(general_recommendation, "DejaVuSans", 11, width - 80)
    for line in wrapped_text:
        c.drawString(40, y_position, line)
        y_position -= 14

        if y_position < 50:  # Если достигли нижнего края страницы, создаем новую
            draw_page_number(c, page_num, width, height)  # Добавляем номер страницы
            c.showPage()
            page_num += 1
            c.setFont("DejaVuSans", 11)
            y_position = height - 50

    # Раздел "Назначенные рекомендации"
    y_position -= 30
    c.setFont("DejaVuSans-Bold", 12)
    c.drawString(20, y_position, "Назначенные рекомендации:")
    y_position -= 20

    for disease in diseases:
        recommendation = recommendations.get(disease, "Нет данных")

        # Выделяем название заболевания жирным шрифтом
        c.setFont("DejaVuSans-Bold", 11)
        c.drawString(40, y_position, f"{disease}:")
        y_position -= 16

        # Основной текст рекомендации
        c.setFont("DejaVuSans", 11)
        wrapped_text = simpleSplit(recommendation, "DejaVuSans", 11, width - 80)
        for line in wrapped_text:
            c.drawString(50, y_position, line)
            y_position -= 14

            if y_position < 50:  # Если достигли нижнего края страницы, создаем новую страницу
                draw_page_number(c, page_num, width, height)  # Добавляем номер страницы
                c.showPage()
                page_num += 1
                c.setFont("DejaVuSans-Bold", 11)
                c.drawString(40, height - 50, f"{disease} (продолжение):")
                y_position = height - 70
                c.setFont("DejaVuSans", 11)

        y_position -= 20  # Отступ между рекомендациями

    # Добавляем номер последней страницы
    draw_page_number(c, page_num, width, height)

    # Завершаем PDF
    c.save()
    return file_path
