# Generated by Django 2.2.4 on 2019-11-24 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrdersApp', '0004_auto_20191124_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='belongs_to_user_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
