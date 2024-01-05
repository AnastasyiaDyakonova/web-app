from django.shortcuts import render


def profile_view(request):
    return render(request, 'main/profile_view.html')

def index(request):
    return render(request, 'main/index.html')

def manager(request):
    return render(request, 'main/manager.html')

def driver(request):
    return render(request, 'main/driver.html')


