
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Задается тип автоинкрементного первичного ключа, который будет использоваться моделями в приложении.
    Этот класс конфигурации соответствует приложению Django с именем «users».
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
