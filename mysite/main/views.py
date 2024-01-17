from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import driver_reportForm, catalog_route_urlForm, manager_taskForm, driver_step_routeForm
from .models import driver_report
from django.db import connection
from django.http import HttpResponse
from .scripts.scheduler import start_scheduler, stop_scheduler

def create(request):
    error = ''
    if request.method == 'POST':
        form = driver_reportForm(request.POST, request.FILES)

        if form.is_valid():
            obj = driver_report.objects.create(
                task_number=form.cleaned_data.get("task_number"),
                odometr_from=form.cleaned_data.get("odometr_from"),
                odometr_to=form.cleaned_data.get("odometr_to"),
                check_number=form.cleaned_data.get("check_number"),
                date_check=form.cleaned_data.get("date_check"),
                sum_check=form.cleaned_data.get("sum_check"),
                image_check = request.FILES.get("image_check"),
                date_create_driver_report=form.cleaned_data.get("date_create_driver_report")
                #image_check=form.cleaned_data.get("image_check")
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
        form2 = catalog_route_urlForm(request.POST)

        if form2.is_valid():
            form2.save()
            return redirect('/profile')
        else:
            error = 'Неверно заполнена форма!!!'
    else:
        form2 = catalog_route_urlForm()
    data = {
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
            return redirect('/profile/create')
        else:
            error = 'Неверно заполнена форма!!!'
    else:
        form = driver_step_routeForm()
    data = {
        'form':form,
        'error':error
    }
    return render(request, 'main/step.html', data)

def select_url_route(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from INTERN_TEAM8.select_url_route")
        data = cursor.fetchall()
    return render(request, 'main/select_url_route.html', {'data': data})

def select_catalog_driver(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from INTERN_TEAM8.select_catalog_driver")
        data = cursor.fetchall()
    return render(request, 'main/select_catalog_driver.html', {'data': data})


def select_report(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from INTERN_TEAM8.select_report ")
        data = cursor.fetchall()
    return render(request, 'main/select_report.html', {'data': data})

@login_required
def select_driver_task_url(request):
    current_user = request.user.username
    current_user_f = request.user.first_name
    current_user_l = request.user.last_name
    with connection.cursor() as cursor:
        cursor.execute("""SELECT t1.task_number, t1.number_route, t3.url_route
from INTERN_TEAM8.MAIN_MANAGER_TASK t1 
LEFT JOIN INTERN_TEAM8.MAIN_DRIVER_REPORT t2
ON t1.TASK_NUMBER = t2.TASK_NUMBER 
LEFT JOIN INTERN_TEAM8.MAIN_CATALOG_ROUTE_URL t3
ON t1.NUMBER_ROUTE = t3.NUMBER_ROUTE 
WHERE t2.ID IS NULL 
AND phone_driver = %s""", [current_user])
        data = cursor.fetchall()
    return render(request, 'main/select_driver_task_url.html', {'data': data, 'current_user_f':current_user_f, 'current_user_l':current_user_l})


def start_job(request):
    start_scheduler()
    return HttpResponse("Job started!")

def stop_job(request):
    stop_scheduler()
    return HttpResponse("Job stopped!")