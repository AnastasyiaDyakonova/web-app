from django.urls import path, include
from .views import RegisterView, profile_views, home

app_name = 'users'

urlpatterns = [
    path('profile/', profile_views, name = "profile"),
    path('register/', RegisterView.as_view(), name = "register"),
    path('', home, name = "home"),
    path('', include('main.urls')),
]