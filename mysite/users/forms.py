from django.contrib.auth.forms import UserCreationForm

from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'role')
