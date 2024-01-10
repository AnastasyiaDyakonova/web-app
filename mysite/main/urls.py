from django.urls import path
from .views import create, route, manager_task_view, driver_step_route_view, select_url_route, select_catalog_driver, select_report
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('profile/create', create, name = "create"),
    path('profile/route', route, name = "route"),
    path('profile/task/', manager_task_view, name = "task"),
    path('profile/step', driver_step_route_view, name = "step"),
    path('profile/task/select_url_route', select_url_route, name = "select_url_route"),
    path('profile/task/select_catalog_driver', select_catalog_driver, name="select_catalog_driver"),
    path('profile/task/select_report', select_report, name="select_report"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

