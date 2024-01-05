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
        form = driver_reportForm(request.POST, request.FILES)
        if form.is_valid():
            login = form.cleaned_data.get("login")
            date_and_time_route_from = form.cleaned_data.get("date_and_time_route_from")
            date_and_time_route_to = form.cleaned_data.get("date_and_time_route_to")
            odometr_from = form.cleaned_data.get("odometr_from")
            odometr_to = form.cleaned_data.get("odometr_to")
            date_check = form.cleaned_data.get("date_check")
            sum_check = form.cleaned_data.get("sum_check")
            number_route = form.cleaned_data.get("number_route")
            result_route = form.cleaned_data.get("result_route")
            image_check = form.cleaned_data.get("image_check")
            obj = driver_report.objects.create(
                login=login,
                date_and_time_route_from=date_and_time_route_from,
                date_and_time_route_to=date_and_time_route_to,
                odometr_from=odometr_from,
                odometr_to=odometr_to,
                date_check=date_check,
                sum_check=sum_check,
                number_route=number_route,
                result_route=result_route,
                image_check=image_check
            )
            obj.save()
            return redirect('/profile')
        else:
            error = 'Неверно заполнена форма'
    else:
        form = driver_reportForm()
    data = {
        'form':form,
        'error':error
    }

    return render(request, 'users/create.html', data)

