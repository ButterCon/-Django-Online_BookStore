# Generated by Django 2.2.5 on 2020-11-24 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0007_auto_20201124_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='BookSB_reserves',
            field=models.FloatField(default=0.3),
        ),
    ]
