from django.urls import path
from . import views



urlpatterns = [
    """path('', views.index, name='home'),
    path('profile', views.profile_view, name='profile'),
    path('manager', views.manager, name='manager'),
    path('driver', views.driver, name='driver'),"""
]