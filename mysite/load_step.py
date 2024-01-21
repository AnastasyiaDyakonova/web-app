"""Данный модуль загружает тестовые данные для модели driver_step_route из файла 'main/static/main/excel/point_driver.xlsx' """
import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()


from main.models import driver_step_route


def load_route_data(file_path):
    """Функция принимает путь к файлу Excel в качестве аргумента.
        Считывает данные из Excel-файла.
        Заменяет все значения NaN на None в DataFrame.
        Затем она итерирует по строкам DataFrame и создает объекты driver_step_route,
        используя данные из каждой строки Excel-файла."""
    df = pd.read_excel(file_path, engine='openpyxl')
    df = df.where(pd.notna(df), None)
    for index, row in df.iterrows():
        driver_step_route.objects.create(
            task_number=row['task_number'],
            date_and_time_route_from=row['date_and_time_route_from'],
            point_1=row['point_1'],
            point_2=row['point_2'],
            point_3=row['point_3'],
            point_4=row['point_4'],
            point_5=row['point_5'],
            point_6=row['point_6'],
            point_7=row['point_7'],
            point_8=row['point_8'],
            point_9=row['point_9'],
            point_10=row['point_10'],
            date_and_time_route_to=row['date_and_time_route_to']
        )


if __name__ == '__main__':
    excel_file_path = 'main/static/main/excel/point_driver.xlsx'
    load_route_data(excel_file_path)