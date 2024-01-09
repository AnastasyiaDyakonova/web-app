from django.contrib.auth.forms import UserCreationForm

from .models import Buyer

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = ('username', 'last_name', 'first_name', 'email', 'role')
