from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.urls import reverse_lazy

def home(request):
    return render(request, 'users/home.html')
@login_required
def profile_views(request):
    user = request.user
    current_user = request.user.first_name

    if user.role == 'менеджер':
        return render(request, 'users/manager.html')
    elif user.role == 'водитель':
        return render(request, 'users/driver.html')
    else:
        return render(request, 'users/profile.html', {'current_user':current_user})

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("users:profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
