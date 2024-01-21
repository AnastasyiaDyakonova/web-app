"""Данный модуль загружает тестовые данные для модели manager_task из файла 'main/static/main/excel/task.xlsx' """
import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()


from main.models import manager_task


def load_route_data(file_path):
    """Функция принимает путь к файлу Excel в качестве аргумента.
        Считывает данные из Excel-файла.
        Заменяет все значения NaN на None в DataFrame.
        Затем она итерирует по строкам DataFrame и создает объекты manager_task,
        используя данные из каждой строки Excel-файла."""
    df = pd.read_excel(file_path, engine='openpyxl')
    df = df.where(pd.notna(df), None)
    for index, row in df.iterrows():
        manager_task.objects.create(
            task_number=row['task_number'],
            date_task=row['date_task'],
            phone_manager=row['phone_manager'],
            phone_driver=row['phone_driver'],
            number_route=row['number_route']
        )
if __name__ == '__main__':
    excel_file_path = 'main/static/main/excel/task.xlsx'
    load_route_data(excel_file_path)