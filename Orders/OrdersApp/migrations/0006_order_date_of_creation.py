# Generated by Django 2.2.4 on 2019-11-28 16:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('OrdersApp', '0005_auto_20191124_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_of_creation',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
