from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from datetime import datetime

# Путь к файлу со шрифтом
FONT_PATH = "assets/fonts/DejaVuSans.ttf"

# Проверяем, существует ли шрифт
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Шрифт '{FONT_PATH}' не найден! Скачайте его и поместите в папку 'assets/fonts/'.")

# Регистрируем шрифт DejaVuSans
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))

def generate_pdf(patient_name, diseases, recommendations):
    """
    Генерирует PDF-файл с рекомендациями, используя DejaVuSans (поддержка кириллицы).
    """
    # Создаём папку для сохранения, если её нет
    output_dir = "recommendations"
    os.makedirs(output_dir, exist_ok=True)

    # Формируем имя файла: ФИО_Дата_Номер.pdf
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"{patient_name}_{date_str}.pdf"
    file_path = os.path.join(output_dir, file_name)

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

    # Раздел "Рекомендации"
    y_position = height - 140
    c.setFont("DejaVuSans", 12)
    c.drawString(20, y_position, "Назначенные рекомендации:")
    y_position -= 20

    c.setFont("DejaVuSans", 11)
    for disease in diseases:
        recommendation = recommendations.get(disease, "Нет данных")
        text = f"•  {recommendation}"

        # Автоматический перенос строк
        wrapped_text = text.split("\n")
        for line in wrapped_text:
            c.drawString(40, y_position, line)
            y_position -= 15
            if y_position < 50:  # Если место закончилось — новая страница
                c.showPage()
                c.setFont("DejaVuSans", 11)
                y_position = height - 50

    # Завершаем PDF
    c.save()
    return file_path
