import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.db import connection, transaction

from .tran_dwh_sql import *

tr_dwh = [tr_stg_user, tr_stg_user_del, tr_stg_driver_step_route, tr_stg_driver_step_route_del, tr_stg_driver_report, tr_stg_driver_report_del, tr_stg_catalog_route_url, tr_stg_catalog_route_url_del, tr_stg_manager_task, tr_stg_manager_task_del,
in_stg_user, in_stg_driver_step_route, in_stg_driver_report, in_stg_catalog_route_url, in_stg_manager_task,
in_stg_user_del, in_stg_driver_step_route_del, in_stg_driver_report_del, in_stg_catalog_route_url_del, in_stg_manager_task_del,
in_dwh_user_hist, in_dwh_driver_step_route_hist, in_dwh_driver_report_hist, in_dwh_catalog_route_url_hist, in_dwh_catalog_route_point_hist, in_dwh_manager_task_hist,
mg_dwh_user_hist, mg_dwh_driver_step_route_hist, mg_dwh_driver_report_hist, mg_dwh_catalog_route_url_hist, mg_dwh_catalog_route_point_hist, mg_dwh_manager_task_hist,
ind_dwh_user_hist, ind_dwh_driver_step_route_hist, ind_dwh_driver_report_hist, ind_dwh_catalog_route_url_hist, ind_dwh_catalog_route_point_hist, ind_dwh_manager_task_hist,
upd_dwh_user_hist, upd_dwh_driver_step_route_hist, upd_dwh_driver_report_hist, upd_dwh_catalog_route_url_hist, upd_dwh_catalog_route_point_hist, upd_dwh_manager_task_hist,
mg_meta]

def run():
    for i in tr_dwh:
        with connection.cursor() as cursor:
            with transaction.atomic():
                cursor.execute(i)
            transaction.commit()
