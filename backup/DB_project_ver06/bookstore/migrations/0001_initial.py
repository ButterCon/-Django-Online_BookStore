# Generated by Django 2.2.5 on 2020-11-05 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Book_name', models.CharField(max_length=100)),
                ('Book_price', models.IntegerField(default=0)),
                ('Book_stock', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_id', models.CharField(default='', max_length=50)),
                ('User_pw', models.CharField(max_length=100)),
                ('User_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingBasket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.User')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingDestination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SD_num', models.IntegerField(default=0)),
                ('SD_ba', models.CharField(max_length=100)),
                ('SD_da', models.CharField(max_length=100)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.User')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order_date', models.DateTimeField()),
                ('Order_totalprice', models.IntegerField(default=0)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.User')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CP_kind', models.CharField(max_length=100)),
                ('CP_Used', models.BooleanField(default=0)),
                ('CP_date', models.DateTimeField()),
                ('CP_validity', models.CharField(max_length=100)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.User')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Card_name', models.CharField(max_length=100)),
                ('Card_num', models.IntegerField(default=0)),
                ('Card_date', models.CharField(max_length=100)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.User')),
            ],
        ),
        migrations.CreateModel(
            name='BookSB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.Book')),
                ('ShoppingBasket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.ShoppingBasket')),
            ],
        ),
        migrations.CreateModel(
            name='BookOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BO_count', models.IntegerField(default=0)),
                ('BO_price', models.IntegerField(default=0)),
                ('CP_kind', models.CharField(default='', max_length=100)),
                ('BO_DC_price', models.IntegerField(default=0)),
                ('Book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.Book')),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookstore.Order')),
            ],
        ),
    ]