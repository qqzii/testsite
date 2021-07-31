# Generated by Django 3.2.5 on 2021-07-28 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_cart_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='adress',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер пользователя'),
        ),
    ]