"""
Конфигурация WSGI для проекта mysite.

Она предоставляет вызываемый WSGI как переменную уровня модуля с именем «application».

Дополнительную информацию об этом файле см.
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
