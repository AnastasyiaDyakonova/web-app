from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Buyer(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'manager'),
        ('driver', 'driver'),
    ]
    role = models.CharField(max_length=8, choices=ROLE_CHOICES,default='user', verbose_name=_("role"))

class driver_report(models.Model):
    login = models.CharField('Логин', max_length=50)
    date_and_time_route_from = models.DateTimeField('Дата и время начала маршрута')
    date_and_time_route_to = models.DateTimeField('Дата и время конца маршрута')
    odometr_from = models.BigIntegerField('Одометр на начало маршрута')
    odometr_to = models.BigIntegerField('Одометр на конец маршрута')
    date_check = models.DateField('Дата оплаты чека')
    sum_check = models.FloatField('Сумма чека за бензин')
    #image_check = models.ImageField('Фото чека за бензин', upload_to='images/', default='')
    number_route = models.BigIntegerField('Номер маршрута')
    result_route = models.CharField('Результат прохождения маршрута(Пройден или Не пройден)', max_length=10)

    def __str__(self):
        return self.login
    class Meta:
        verbose_name = 'Отчет водителя'
        verbose_name_plural = "Отчеты водителей"



