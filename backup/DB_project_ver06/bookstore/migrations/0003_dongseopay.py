# Generated by Django 2.2.5 on 2020-11-10 23:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0002_auto_20201109_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='DongseoPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DP_TradingDate', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('DP_ChargePrice', models.IntegerField(default=0)),
                ('DP_UsedPrice', models.IntegerField(default=0)),
                ('DP_price', models.IntegerField(default=0)),
                ('DP_history', models.IntegerField(default=0)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.User')),
            ],
        ),
    ]