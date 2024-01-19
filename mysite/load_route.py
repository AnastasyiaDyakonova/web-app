import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()

from main.models import catalog_route_url


def load_route_data(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')

    # Заменяем все значения NaN на None
    df = df.where(pd.notna(df), None)

    for index, row in df.iterrows():
        catalog_route_url.objects.create(
            number_route=row['number_route'],
            count_point_to_route=row['count_point_to_route'],
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
            url_route=row['url_route'],
            date_create_route=row['date_create_route']
        )


if __name__ == '__main__':
    excel_file_path = 'main/static/main/excel/catalog_route.xlsx'
    load_route_data(excel_file_path)