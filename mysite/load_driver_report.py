import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()


from main.models import driver_report


def load_route_data(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')

    # Заменяем все значения NaN на None
    df = df.where(pd.notna(df), None)

    for index, row in df.iterrows():
        driver_report.objects.create(
            task_number=row['task_number'],
            odometr_from=row['odometr_from'],
            odometr_to=row['odometr_to'],
            check_number=row['check_number'],
            date_check=row['date_check'],
            sum_check=row['sum_check'],
            image_check=row['image_check'],
            date_create_driver_report=row['date_create_driver_report']
        )


if __name__ == '__main__':
    excel_file_path = 'main/static/main/excel/driver_report.xlsx'
    load_route_data(excel_file_path)