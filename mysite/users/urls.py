from django.urls import path
from .views import RegisterView, profile_views, create

app_name = 'users'

urlpatterns = [
    path('profile/', profile_views, name = "profile"),
    path('register/', RegisterView.as_view(), name = "register"),
    path('profile/create', create, name = "create"),
]