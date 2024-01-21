"""
Конфигурация ASGI для проекта mysite.

Она предоставляет вызываемый ASGI как переменную уровня модуля с именем «application».

Дополнительную информацию об этом файле см.
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_asgi_application()
