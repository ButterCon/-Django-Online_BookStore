# Generated by Django 2.2.5 on 2020-11-24 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0011_auto_20201124_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Order_Reserves_totalprice',
            field=models.IntegerField(default=0),
        ),
    ]
