# Generated by Django 3.2.6 on 2021-08-10 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20210810_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notebook',
            name='date',
        ),
    ]
