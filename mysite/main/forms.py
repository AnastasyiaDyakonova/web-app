from django.forms import Form, ModelForm, TextInput, DateTimeInput, NumberInput, DateInput, FileInput, URLInput, \
    CheckboxInput
from .models import driver_report, catalog_route_url, manager_task, driver_step_route


class driver_reportForm(ModelForm):
    class Meta:
        model = driver_report
        fields = ['task_number', 'odometr_from', 'odometr_to', 'check_number', 'date_check', 'sum_check', 'image_check', 'date_create_driver_report']

        widgets = {
            "task_number": NumberInput(attrs={'id': 'task_number', 'name': 'task_number', 'required':''}),
            "odometr_from": NumberInput(attrs={'id': 'odometr_from', 'name': 'odometr_from', 'required':''}),
            "odometr_to": NumberInput(attrs={'id': 'odometr_to', 'name': 'odometr_to', 'required':'' }),
            "check_number": NumberInput(attrs={'id': 'check_number', 'name': 'check_number', 'required': ''}),
            "date_check": DateInput(attrs={'id': 'date_check', 'name': 'date_check', 'type': 'date', 'required':''}),
            "sum_check": NumberInput(attrs={'id': 'sum_check', 'name': 'sum_check', 'required':''}),
            "image_check": FileInput(attrs={'id': 'image_check', 'name': 'file', 'required':''}),
            "date_create_driver_report": DateInput(attrs={'id': 'date_create_driver_report', 'name': 'date_create_driver_report', 'type': 'date','required': ''})
        }


class catalog_route_urlForm(ModelForm):
    class Meta:
        model = catalog_route_url
        fields = ['number_route', 'count_point_to_route', 'point_1', 'point_2', 'point_3', 'point_4', 'point_5', 'point_6', 'point_7', 'point_8', 'point_9', 'point_10', 'url_route', 'date_create_route']

        widgets = {
            "number_route": TextInput(attrs={'id': 'catalog_route', 'name': 'catalog_route', 'required': '' }),
            "count_point_to_route": NumberInput(attrs={'id': 'count_point_to_route', 'name': 'count_point_to_route', 'required': '' }),
            "point_1": TextInput(attrs={'id': 'point_1', 'name': 'point_1', 'required': ""}),
            "point_2": TextInput(attrs={'id': 'point_2', 'name': 'point_2', 'required': False}),
            "point_3": TextInput(attrs={'id': 'point_3', 'name': 'point_3', 'required': False}),
            "point_4": TextInput(attrs={'id': 'point_4', 'name': 'point_4', 'required': False}),
            "point_5": TextInput(attrs={'id': 'point_5', 'name': 'point_5', 'required': False}),
            "point_6": TextInput(attrs={'id': 'point_6', 'name': 'point_6', 'required': False}),
            "point_7": TextInput(attrs={'id': 'point_7', 'name': 'point_7', 'required': False}),
            "point_8": TextInput(attrs={'id': 'point_8', 'name': 'point_8', 'required': False}),
            "point_9": TextInput(attrs={'id': 'point_9', 'name': 'point_9', 'required': False}),
            "point_10": TextInput(attrs={'id': 'point_10', 'name': 'point_10', 'required': False}),
            "url_route": URLInput(attrs={'id': 'url_route', 'name': 'url_route', 'required': '' }),
            "date_create_route": DateInput(attrs={'id': 'date_create_route', 'name': 'date_create_route', 'type': 'date', 'required':''})
        }

class manager_taskForm(ModelForm):
    class Meta:
        model = manager_task
        fields = ['task_number', 'date_task', 'phone_manager', 'phone_driver', 'number_route']

        widgets = {
            "task_number": NumberInput(attrs={'id': 'task_number', 'name': 'task_number', 'required':'' }),
            "date_task": DateInput(attrs={'id': 'date_task', 'name': 'date_task', 'type': 'date', 'required': ''}),
            "phone_manager": TextInput(attrs={'id': 'phone_manager', 'name': 'phone_manager', 'required': '' }),
            "phone_driver": TextInput(attrs={'id': 'phone_driver', 'name': 'phone_driver', 'required': '' }),
            "number_route": TextInput(attrs={'id': 'number_route', 'name': 'number_route', 'required': ''})}

class driver_step_routeForm(ModelForm):

    class Meta:
        model = driver_step_route
        fields = ['task_number', 'date_and_time_route_from', 'point_1', 'point_2', 'point_3', 'point_4', 'point_5', 'point_6', 'point_7', 'point_8', 'point_9', 'point_10','date_and_time_route_to']

        widgets = {"task_number": NumberInput(attrs={'id': 'task_number', 'name': 'task_number','required':''}),
                   "date_and_time_route_from": DateTimeInput(attrs={'id': 'date_and_time_route_from', 'name': 'date_and_time_route_from', 'type': 'datetime-local', 'required': ''}),
                   "point_1": CheckboxInput(attrs={'id': 'point_1', 'name': 'point_1', 'required': False}),
                   "point_2": CheckboxInput(attrs={'id': 'point_2', 'name': 'point_2', 'required': False}),
                   "point_3": CheckboxInput(attrs={'id': 'point_3', 'name': 'point_3', 'required': False}),
                   "point_4": CheckboxInput(attrs={'id': 'point_4', 'name': 'point_4', 'required': False}),
                   "point_5": CheckboxInput(attrs={'id': 'point_5', 'name': 'point_5', 'required': False}),
                   "point_6": CheckboxInput(attrs={'id': 'point_6', 'name': 'point_6', 'required': False}),
                   "point_7": CheckboxInput(attrs={'id': 'point_7', 'name': 'point_7', 'required': False}),
                   "point_8": CheckboxInput(attrs={'id': 'point_8', 'name': 'point_8', 'required': False}),
                   "point_9": CheckboxInput(attrs={'id': 'point_9', 'name': 'point_9', 'required': False}),
                   "point_10": CheckboxInput(attrs={'id': 'point_10', 'name': 'point_10', 'required': False}),
                   "date_and_time_route_to": DateTimeInput(attrs={'id': 'date_and_time_route_to', 'name': 'date_and_time_route_to', 'type': 'datetime-local', 'required': ''})}

