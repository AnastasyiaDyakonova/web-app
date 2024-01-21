"""В данном модуле определяются шаблоны URL-адресов для различных представлений.
Модуль включает в себя необходимую конфигурацию для обслуживания статических файлов."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


