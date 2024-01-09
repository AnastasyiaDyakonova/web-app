from django.shortcuts import render, redirect

from .forms import driver_reportForm, catalog_routeForm, catalog_route_urlForm, manager_taskForm, driver_step_routeForm
from .models import driver_report


def create(request):
    error = ''
    if request.method == 'POST':
        form = driver_reportForm(request.POST, request.FILES)

        if form.is_valid():
            obj = driver_report.objects.create(
                task_number=form.cleaned_data.get("task_number"),
                date_and_time_task=form.cleaned_data.get("date_and_time_task"),
                phone_manager=form.cleaned_data.get("phone_manager"),
                phone_driver=form.cleaned_data.get("phone_driver"),
                date_and_time_route_from=form.cleaned_data.get("date_and_time_route_from"),
                date_and_time_route_to=form.cleaned_data.get("date_and_time_route_to"),
                odometr_from=form.cleaned_data.get("odometr_from"),
                odometr_to=form.cleaned_data.get("odometr_to"),
                date_check=form.cleaned_data.get("date_check"),
                sum_check=form.cleaned_data.get("sum_check"),
                number_route=form.cleaned_data.get("number_route"),
                result_route=form.cleaned_data.get("result_route"),
                image_check=form.cleaned_data.get("image_check")
            )
            obj.save()
            return redirect('/profile')
        else:
            error = 'Неверно заполнена форма!!!'
    else:
        form = driver_reportForm()
    data = {
        'form':form,
        'error':error
    }

    return render(request, 'main/create.html', data)




def route(request):
    error = ''
    if request.method == 'POST':
        form2 = catalog_routeForm(request.POST)
        form1 = catalog_route_urlForm(request.POST)

        if form1.is_valid() and form2.save():
            form1.save()
            form2.save()
            return redirect('/profile')
        else:
            error = 'Неверно заполнена форма!!!'

    else:
        form2 = catalog_routeForm()
        form1 = catalog_route_urlForm()
    data = {
        'form1':form1,
        'form2': form2,
        'error':error
    }

    return render(request, 'main/route.html', data)


def manager_task_view(request):
    error = ''
    if request.method == 'POST':
        form3 = manager_taskForm(request.POST)

        if form3.is_valid() :
            form3.save()
            return redirect('/profile')
        else:
            error = 'Неверно заполнена форма!!!'
    else:
        form3 = manager_taskForm()
    data = {
        'form3':form3,
        'error':error
    }
    return render(request, 'main/task.html', data)


def driver_step_route_view(request):
    error = ''
    if request.method == 'POST':
        form = driver_step_routeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/profile')
        else:
            error = 'Неверно заполнена форма!!!'
    else:
        form = driver_step_routeForm()
    data = {
        'form':form,
        'error':error
    }
    return render(request, 'main/step.html', data)
