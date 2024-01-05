from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm, driver_reportForm
from django.urls import reverse_lazy

from .models import driver_report


@login_required
def profile_views(request):
    user = request.user
    if user.role == 'manager':
        return render(request, 'users/manager.html')
    elif user.role == 'driver':
        return render(request, 'users/driver.html')
    else:
        return render(request, 'users/profile.html')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("users:profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def create(request):
    error = ''
    if request.method == 'POST':
        form = driver_reportForm(request.POST) #, request.FILES)
        if form.is_valid():
            """name = form.cleaned_data.get("login")
            img = form.cleaned_data.get("image_check")
            obj = driver_report.objects.create(
                title=name,
                img=img
            )
            obj.save()
            print(obj)"""
            form.save()
            return redirect('/profile')
        else:
            error = 'Неверно заполнена форма'
    form = driver_reportForm()
    data = {
        'form':form,
        'error':error
    }

    return render(request, 'users/create.html', data)

