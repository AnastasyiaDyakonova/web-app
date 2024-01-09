from django.urls import path
from .views import create, route, manager_task_view, driver_step_route_view

urlpatterns = [
    path('profile/create', create, name = "create"),
    path('profile/route', route, name = "route"),
    path('profile/task', manager_task_view, name = "task"),
    path('profile/step', driver_step_route_view, name = "step"),
]

