""" В данном модуле настраивается основной интерфейс для созданных моделей, прописываются нужные поля, настраиваются виджеты."""
from django.contrib.auth.forms import UserCreationForm

from .models import User

class RegisterForm(UserCreationForm):
    """Создается форма для модели User."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'role')
