from django.shortcuts import render, redirect

from .forms import driver_reportForm, catalog_route_urlForm, manager_taskForm, driver_step_routeForm
from .models import driver_report
from django.db import connection

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
        cursor.execute("select number_route, url_route from INTERN_TEAM8.main_catalog_route_url ;")
        data = cursor.fetchall()
    return render(request, 'main/select_url_route.html', {'data': data})

def select_catalog_driver(request):
    with connection.cursor() as cursor:
        cursor.execute("""select first_name, 
                                  last_name, 
                                  username, 
                                  email 
                            from INTERN_TEAM8.users_user
                            where role='водитель';""")
        data = cursor.fetchall()
    return render(request, 'main/select_catalog_driver.html', {'data': data})


def select_report(request):
    with connection.cursor() as cursor:
        cursor.execute("""select '№'|| t1.task_number || ' от ' || to_char(t1.date_task, 'dd.mm.yyyy') as number_date__task,  
	   t5.first_name || ' ' ||  t5.last_name as FI, 
	   t5.username,
	   t2.date_and_time_route_to - t2.date_and_time_route_from as time_route,
	   t3.odometr_to - t3.odometr_from as distance_km,
	   '№'|| t3.check_number || ' от ' || to_char(t3.date_check, 'dd.mm.yyyy') as number_date_and_time_check,
	   t3.sum_check, 
	   t3.image_check,
	   case 
	   	when (t2.point_1 + t2.point_2 + t2.point_3 + t2.point_4 + t2.point_5 + t2.point_6 + t2.point_7 + t2.point_8 + t2.point_9 + t2.point_10) = count_point_to_route then 'Пройден'
	   else 'Не пройден'
	   end result,
	   t1.number_route,
	   t4.url_route
from INTERN_TEAM8.main_manager_task t1
left join INTERN_TEAM8.main_driver_step_route t2
on t1.task_number = t2.task_number
left join INTERN_TEAM8.main_driver_report t3
on t2.task_number = t3.task_number 
left join INTERN_TEAM8.main_catalog_route_url t4
on t1.number_route = t4.number_route 
left join INTERN_TEAM8.users_user t5
on t1.phone_driver = t5.username 
""")
        data = cursor.fetchall()
    return render(request, 'main/select_report.html', {'data': data})