from django.forms import Form, ModelForm, TextInput, DateTimeInput, NumberInput, DateInput, FileInput, URLInput, \
    CheckboxInput
from .models import driver_report, catalog_route_url, catalog_route, manager_task, driver_step_route


class driver_reportForm(ModelForm):
    class Meta:
        model = driver_report
        fields = ['task_number', 'date_and_time_task', 'phone_manager', 'phone_driver', 'date_and_time_route_from', 'date_and_time_route_to', 'odometr_from', 'odometr_to', 'date_check', 'sum_check', 'number_route', 'result_route', 'image_check']

        widgets = {
            "task_number": NumberInput(attrs={
                'id': 'task_number',
                'name': 'task_number',
                'required':''
            }),
            "date_and_time_task": DateTimeInput(attrs={
                'id': 'date_and_time_task',
                'name': 'date_and_time_task',
                'required': ''
            }),
            "phone_manager": TextInput(attrs={
                'id': 'phone_manager',
                'name': 'phone_manager',
                'required': ''
            }),
            "phone_driver": TextInput(attrs={
                'id': 'phone_driver',
                'name': 'phone_driver',
                'required':''
            }),
            "date_and_time_route_from": DateTimeInput(attrs={
                'id': 'date_and_time_route_from',
                'name': 'date_and_time_route_from',
                'required':''
            }),
            "date_and_time_route_to": DateTimeInput(attrs={
                'id': 'date_and_time_route_to',
                'name': 'date_and_time_route_to',
                'required':''
            }),
            "odometr_from": NumberInput(attrs={
                'id': 'odometr_from',
                'name': 'odometr_from',
                'required':''
            }),
            "odometr_to": NumberInput(attrs={
                'id': 'odometr_to',
                'name': 'odometr_to',
                'required':''
            }),
            "date_check": DateInput(attrs={
                'id': 'date_check',
                'name': 'date_check',
                'required':''
            }),
            "sum_check": NumberInput(attrs={
                'id': 'sum_check',
                'name': 'sum_check',
                'required':''
            }),
           "image_check": FileInput(attrs={
                'id': 'image_check',
                'name': 'image_check',
                'required':''
            }),
            "number_route": NumberInput(attrs={
                'id': 'number_route',
                'name': 'number_route',
                'required':''
            }),
            "result_route": TextInput(attrs={
                'id': 'result_route',
                'name': 'result_route',
                'required':''
            })
        }


class catalog_route_urlForm(ModelForm):
    class Meta:
        model = catalog_route_url
        fields = ['number_route', 'url_route']

        widgets = {
            "number_route": TextInput(attrs={
                'id': 'catalog_route',
                'name': 'catalog_route',
                'required': ''
            }),
            "url_route": URLInput(attrs={
                'id': 'url_route',
                'name': 'url_route',
                'required': ''
            })
        }
class catalog_routeForm(ModelForm):
    class Meta:
        model = catalog_route
        fields = ['number_route', 'number_point', 'latitude', 'longitude']

        widgets = {
            "number_route": TextInput(attrs={
                'id': 'number_route',
                'name': 'number_route'
            }),
            "number_point": TextInput(attrs={
                'id': 'number_point',
                'name': 'number_point',
                'required': ''
            }),
            "latitude": NumberInput(attrs={
                'id': 'latitude',
                'name': 'latitude',
                'required': ''
            }),
            "longitude": NumberInput(attrs={
                'id': 'longitude',
                'name': 'longitude',
                'required': ''
            })
        }

class manager_taskForm(ModelForm):
    class Meta:
        model = manager_task
        fields = ['task_number', 'date_and_time_task', 'phone_manager', 'phone_driver', 'number_route']

        widgets = {
            "task_number": NumberInput(attrs={'id': 'task_number', 'name': 'task_number', 'required':'' }),
            "date_and_time_task": DateTimeInput(attrs={'id': 'date_and_time_task', 'name': 'date_and_time_task', 'required': ''}),
            "phone_manager": TextInput(attrs={'id': 'phone_manager', 'name': 'phone_manager', 'required': '' }),
            "phone_driver": TextInput(attrs={'id': 'phone_driver', 'name': 'phone_driver', 'required': '' }),
            "number_route": TextInput(attrs={'id': 'number_route', 'name': 'number_route', 'required': ''})}

class driver_step_routeForm(ModelForm):

    class Meta:
        model = driver_step_route
        fields = ['task_number', 'date_and_time_route_from', 'point_1', 'point_2', 'point_3', 'point_4', 'point_5', 'point_6', 'point_7', 'point_8', 'point_9', 'point_10','date_and_time_route_to']

        widgets = {"task_number": NumberInput(attrs={'id': 'task_number', 'name': 'task_number','required':''}),
                   "date_and_time_route_from": DateTimeInput(attrs={'id': 'date_and_time_route_from', 'name': 'date_and_time_route_from', 'required': ''}),
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
                   "date_and_time_route_to": DateTimeInput(attrs={'id': 'date_and_time_route_to', 'name': 'date_and_time_route_to', 'required': ''})}

"""class catalog_routeForm(ModelForm):
    class Meta:
        model = catalog_route
        fields = ['number_route', 'number_point', 'latitude', 'longitude']
        widgets = {"number_route": TextInput(attrs={}),"number_point": TextInput(attrs={}),"latitude": NumberInput(attrs={}),"longitude":NumberInput(attrs={})}
class catalog_route_urlForm(ModelForm):
    class Meta:
        model = catalog_route_url
        fields = [ 'number_route', 'url_route']
        widgets = {"number_route": TextInput(attrs={}), "url_route": URLInput(attrs={})}"""