# Generated by Django 4.2.8 on 2024-01-08 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_driver_step_route_manager_task_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager_task',
            name='date_and_time_task',
            field=models.DateTimeField(verbose_name='Дата и время задачи'),
        ),
    ]
