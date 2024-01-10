from django.db import models

class driver_report(models.Model):
    task_number = models.BigIntegerField('Номер задачи')
    odometr_from = models.BigIntegerField('Одометр на начало маршрута')
    odometr_to = models.BigIntegerField('Одометр на конец маршрута')
    check_number = models.BigIntegerField('Номер чека')
    date_check = models.DateField('Дата оплаты чека')
    sum_check = models.FloatField('Сумма чека за бензин')
    image_check = models.ImageField('Фото чека за бензин', upload_to='images/')

    def __str__(self):
        return self.task_number
    class Meta:
        verbose_name = 'Отчет водителя'
        verbose_name_plural = "Отчеты водителей"

class catalog_route_url(models.Model):
    number_route = models.CharField('Номер маршрута', max_length=7, primary_key=True)
    point_1 = models.CharField('Точка 1', max_length=20)
    point_2 = models.CharField('Точка 2', max_length=20, blank=True)
    point_3 = models.CharField('Точка 3', max_length=20, blank=True)
    point_4 = models.CharField('Точка 4', max_length=20, blank=True)
    point_5 = models.CharField('Точка 5', max_length=20, blank=True)
    point_6 = models.CharField('Точка 6', max_length=20, blank=True)
    point_7 = models.CharField('Точка 7', max_length=20, blank=True)
    point_8 = models.CharField('Точка 8', max_length=20, blank=True)
    point_9 = models.CharField('Точка 9', max_length=20, blank=True)
    point_10 = models.CharField('Точка 10', max_length=20, blank=True)
    url_route = models.URLField(verbose_name='Ссылка на маршрут', max_length = 500)
    class Meta:
        verbose_name = 'URL-адрес'
        verbose_name_plural = "URL-адреса"

class manager_task(models.Model):
    task_number = models.BigIntegerField('Номер задачи', primary_key=True)
    date_and_time_task = models.DateTimeField('Дата и время задачи')
    phone_manager = models.CharField('Телефон менеджера', max_length=11)
    phone_driver = models.CharField('Телефон водителя', max_length=11)
    number_route = models.CharField('Номер маршрута', max_length=7)
    class Meta:
        verbose_name = 'Задача от менеджера'
        verbose_name_plural = "Задачи от менеджера"

class driver_step_route(models.Model):
    task_number = models.BigIntegerField('Номер задачи', primary_key=True)
    date_and_time_route_from = models.DateTimeField('Дата и время начала маршрута')
    point_1 = models.BooleanField('Точка 1', default=False, blank=True)
    point_2 = models.BooleanField('Точка 2', default=False, blank=True)
    point_3 = models.BooleanField('Точка 3', default=False, blank=True)
    point_4 = models.BooleanField('Точка 4', default=False, blank=True)
    point_5 = models.BooleanField('Точка 5', default=False, blank=True)
    point_6 = models.BooleanField('Точка 6', default=False, blank=True)
    point_7 = models.BooleanField('Точка 7', default=False, blank=True)
    point_8 = models.BooleanField('Точка 8', default=False, blank=True)
    point_9 = models.BooleanField('Точка 9', default=False, blank=True)
    point_10 = models.BooleanField('Точка 10', default=False, blank=True)
    date_and_time_route_to = models.DateTimeField('Дата и время конца маршрута')

    class Meta:
        verbose_name = 'Прохождение маршрута'
        verbose_name_plural = "Прохождение маршрутов"













"""class catalog_route_url(models.Model):
    number_route = models.CharField('Номер маршрута', max_length=7, primary_key=True)
    url_route = models.URLField(verbose_name='Ссылка на маршрут')
    class Meta:
        verbose_name = 'Справочник url-адресов'
        verbose_name_plural = "Справочник url-адресов"

class catalog_route(models.Model):
    number_route = models.ForeignKey(catalog_route_url, on_delete=models.CASCADE)
    number_point = models.CharField('Номер точки', max_length=7)
    latitude = models.DecimalField('Широта', max_digits=8, decimal_places=6)
    longitude = models.DecimalField('Долгота', max_digits=8, decimal_places=6)
    class Meta:
        verbose_name = 'Справочник маршрутов'
        verbose_name_plural = "Справочник маршрутов"
"""