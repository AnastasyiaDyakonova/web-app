# Generated by Django 4.2.8 on 2024-01-04 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_driver_report_image_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver_report',
            name='image_check',
            field=models.FileField(upload_to='users/image/', verbose_name='Фото чека за бензин'),
        ),
    ]
