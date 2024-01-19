import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()


from main.models import manager_task


def load_route_data(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')

    # Заменяем все значения NaN на None
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