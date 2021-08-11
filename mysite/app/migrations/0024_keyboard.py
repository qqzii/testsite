# Generated by Django 3.2.6 on 2021-08-11 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_mouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('market_date', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дата выхода на рынок')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип')),
                ('switch_technology', models.CharField(blank=True, max_length=255, null=True, verbose_name='Технология переключателя')),
                ('appointment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Назначение')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='Цвет')),
                ('connection_interface', models.CharField(blank=True, max_length=255, null=True, verbose_name='Интерфейс подключения клавиатуры')),
                ('digital_block', models.CharField(blank=True, max_length=255, null=True, verbose_name='Цифровой блок')),
                ('wire_length', models.CharField(blank=True, max_length=255, null=True, verbose_name='Длина провода')),
                ('body_material', models.CharField(blank=True, max_length=255, null=True, verbose_name='Материал корпуса')),
                ('additional_buttons', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дополнительные кнопки')),
                ('key_shape', models.CharField(blank=True, max_length=255, null=True, verbose_name='Форма клавиш')),
                ('switch_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип переключателя')),
                ('built_in_memory', models.CharField(blank=True, max_length=255, null=True, verbose_name='Встроенная память')),
                ('key_illumination', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подсветка клавиш')),
                ('wire_braid', models.CharField(blank=True, max_length=255, null=True, verbose_name='Оплетка провода')),
                ('usb', models.CharField(blank=True, max_length=255, null=True, verbose_name='USB-порт')),
                ('audio_input', models.CharField(blank=True, max_length=255, null=True, verbose_name='Аудиовход')),
                ('audio_output', models.CharField(blank=True, max_length=255, null=True, verbose_name='Аудиовыход')),
                ('width', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ширина')),
                ('depth', models.CharField(blank=True, max_length=255, null=True, verbose_name='Глубина')),
                ('thickness', models.CharField(blank=True, max_length=255, null=True, verbose_name='Толщина')),
                ('weight', models.CharField(blank=True, max_length=255, null=True, verbose_name='Вес')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
