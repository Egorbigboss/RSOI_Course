# Generated by Django 2.2.4 on 2019-11-28 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DeliveryApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverylist',
            name='order_uuid',
            field=models.UUIDField(null=True),
        ),
    ]