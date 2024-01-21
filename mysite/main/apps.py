from django.apps import AppConfig


class MainConfig(AppConfig):
    """
    Задается тип автоинкрементного первичного ключа, который будет использоваться моделями в приложении.
    Этот класс конфигурации соответствует приложению Django с именем «main».
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
