from django.urls import path
from .views import create, route, manager_task_view, driver_step_route_view, select_url_route, select_catalog_driver, \
    select_report, start_job, stop_job, select_driver_task_url, success, select_dwh_report, select_itog_report, \
    export_to_excel_task, export_to_excel_itog
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('profile/create', create, name = "create"),
    path('profile/route', route, name = "route"),
    path('profile/task/', manager_task_view, name = "task"),
    path('profile/step', driver_step_route_view, name = "step"),
    path('profile/select_driver_task_url', select_driver_task_url, name = "select_driver_task_url"),
    path('profile/task/select_url_route', select_url_route, name = "select_url_route"),
    path('profile/task/select_catalog_driver', select_catalog_driver, name="select_catalog_driver"),
    path('profile/task/select_report', select_report, name="select_report"),
    path('success/', success, name='success'),
    path('profile/select_dwh_report', select_dwh_report, name = "select_dwh_report"),
    path('profile/select_dwh_report/export_to_excel_task', export_to_excel_task, name = "export_to_excel_task"),
    path('profile/select_dwh_report/export_to_excel_itog', export_to_excel_itog, name="export_to_excel_itog"),
    path('profile/select_itog_report', select_itog_report, name = "select_itog_report"),
    path('start_job/', start_job, name='start_job'),
    path('stop_job/', stop_job, name='stop_job'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


