"""В данном модуле создаются представления, которые будут выполнять логику проекта."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.urls import reverse_lazy

def home(request):
    """Данная функция возвращает страницу users/home.html"""
    return render(request, 'users/home.html')
@login_required
def profile_views(request):
    """Если пользователь зарегистрирован, данная функция возвращает:

     1. страницу users/manager.html - если пользователь зарегистрирован как менеджер;

     2. страницу users/driver.html - если пользователь зарегистрирован как водитель;

     3. страницу users/profile.html - если пользователь не зарегистрирован ни как менеджер, ни как водитель.

     """
    user = request.user
    if user.role == 'менеджер':
        return render(request, 'users/manager.html')
    elif user.role == 'водитель':
        return render(request, 'users/driver.html')
    else:
        return render(request, 'users/profile.html')

class RegisterView(FormView):
    """Представление для регистрации пользователя с помощью формы."""
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("users:profile")
    def form_valid(self, form):
        """Данная функция проверяет валидность введенных данных при регистрации, сохраняет данные,
        перенаправляет на страницу входа в профиль.
             """
        form.save()
        return super().form_valid(form)
