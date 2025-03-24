import json
import os
from ui import RecommendationApp

JSON_FILE = "recommendations.json"
OUTPUT_FOLDER = "recommendations"

class Logic:
    @staticmethod
    def generate_recommendations(name, selected_diseases):
        """Генерирует файл рекомендаций"""
        recommendations = Logic.load_recommendations()

        # Создаём папку, если её нет
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # Формируем содержимое файла
        file_content = f"Пациент: {name}\n\nРекомендации:\n"
        for disease in selected_diseases:
            recommendation = recommendations.get(disease, "Нет рекомендаций")
            file_content += f"- {disease}: {recommendation}\n"

        # Сохраняем файл
        file_path = os.path.join(OUTPUT_FOLDER, f"{name}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)

    @staticmethod
    def add_recommendation(disease, recommendation):
        """Добавляет болезнь в JSON"""
        recommendations = Logic.load_recommendations()
        recommendations[disease] = recommendation

        # Записываем в JSON
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(recommendations, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_recommendations():
        """Загружает JSON-файл с рекомендациями"""
        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

# Запуск приложения
if __name__ == "__main__":
    app = RecommendationApp(Logic)
    app.mainloop()
