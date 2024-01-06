from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Buyer(AbstractUser):
    ROLE_CHOICES = [
        ('менеджер', 'manager'),
        ('водитель', 'driver'),
    ]
    role = models.CharField(max_length=8, choices=ROLE_CHOICES,default='user', verbose_name=_("role"))

class driver_report(models.Model):
    task_number = models.BigIntegerField('Номер задачи')
    date_and_time_task = models.DateTimeField('Дата и время задачи')
    phone_manager = models.CharField('Телефон менеджера', max_length=11)
    phone_driver = models.CharField('Телефон водителя', max_length=11)
    date_and_time_route_from = models.DateTimeField('Дата и время начала маршрута')
    date_and_time_route_to = models.DateTimeField('Дата и время конца маршрута')
    odometr_from = models.BigIntegerField('Одометр на начало маршрута')
    odometr_to = models.BigIntegerField('Одометр на конец маршрута')
    date_check = models.DateField('Дата оплаты чека')
    sum_check = models.FloatField('Сумма чека за бензин')
    image_check = models.ImageField('Фото чека за бензин', upload_to='images/')
    number_route = models.BigIntegerField('Номер маршрута')
    result_route = models.CharField('Результат прохождения маршрута(Пройден или Не пройден)', max_length=10)

    def __str__(self):
        return self.phone_driver
    class Meta:
        verbose_name = 'Отчет водителя'
        verbose_name_plural = "Отчеты водителей"



