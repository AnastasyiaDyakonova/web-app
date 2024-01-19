import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()


from users.models import User


def load_route_data(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')

    # Заменяем все значения NaN на None
    df = df.where(pd.notna(df), None)

    for index, row in df.iterrows():
        User.objects.create(
            id=row['id'],
            password=row['password'],
            last_login=row['last_login'],
            is_superuser=row['is_superuser'],
            username=row['username'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            is_staff=row['is_staff'],
            is_active=row['is_active'],
            date_joined=row['date_joined'],
            role=row['role']
        )


if __name__ == '__main__':
    excel_file_path = 'main/static/main/excel/user.xlsx'
    load_route_data(excel_file_path)