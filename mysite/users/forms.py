from django.contrib.auth.forms import UserCreationForm
from .models import Buyer, driver_report
from django.forms import ModelForm, TextInput,  DateTimeInput, NumberInput, DateInput, FileInput


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Buyer
        fields = ('username', 'last_name', 'first_name', 'email', 'role')


class driver_reportForm(ModelForm):
    class Meta:
        model = driver_report
        fields = ['login', 'date_and_time_route_from', 'date_and_time_route_to', 'odometr_from', 'odometr_to', 'date_check', 'sum_check', 'number_route', 'result_route', 'image_check']

        widgets = {
            "login": TextInput(attrs={
                'id': 'login',
                'name': 'login',
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