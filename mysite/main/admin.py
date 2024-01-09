from django.contrib import admin

from .models import driver_report, catalog_route_url, catalog_route, manager_task, driver_step_route

# Register your models here.

admin.site.register(driver_report)
admin.site.register(catalog_route_url)
admin.site.register(catalog_route)
admin.site.register(manager_task)
admin.site.register(driver_step_route)
