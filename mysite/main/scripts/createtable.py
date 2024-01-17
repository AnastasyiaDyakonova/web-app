import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.db import connection

from .createdwh import *



cr_dwh = [cr_meta, cr_stg_user, cr_stg_user_del, cr_dwh_user_hist, cr_stg_driver_step_route, cr_stg_driver_step_route_del, cr_dwh_driver_step_route_hist, cr_stg_driver_report, cr_stg_driver_report_del, cr_dwh_driver_report_hist, cr_stg_catalog_route_url, cr_stg_catalog_route_url_del, cr_dwh_catalog_route_url_hist, cr_dwh_catalog_route_point_hist, cr_stg_manager_task, cr_stg_manager_task_del, cr_dwh_manager_task_hist, cr_view_select_url_route, cr_view_select_catalog_driver, cr_view_select_report]
def run():
    for i in cr_dwh:
        with connection.cursor() as cursor:
            cursor.execute(i)