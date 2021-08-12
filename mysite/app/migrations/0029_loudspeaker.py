# Generated by Django 3.2.6 on 2021-08-11 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_monitor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loudspeaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('market_date', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дата выхода на рынок')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип')),
                ('rms', models.CharField(blank=True, max_length=255, null=True, verbose_name='Номинальная мощность (RMS)')),
                ('supply', models.CharField(blank=True, max_length=255, null=True, verbose_name='Питание')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='Цвет')),
                ('stereo_speakers', models.CharField(blank=True, max_length=255, null=True, verbose_name='Стереодинамики')),
                ('panoramic_audio', models.CharField(blank=True, max_length=255, null=True, verbose_name='Панорамное аудио')),
                ('number_of_stripes', models.CharField(blank=True, max_length=255, null=True, verbose_name='Количество полос')),
                ('number_of_speakers', models.CharField(blank=True, max_length=255, null=True, verbose_name='Количество динамиков')),
                ('number_of_passive_speakers', models.CharField(blank=True, max_length=255, null=True, verbose_name='Количество пассивных динамиков')),
                ('acoustic_design', models.CharField(blank=True, max_length=255, null=True, verbose_name='Акустическое оформление')),
                ('frequency_range', models.CharField(blank=True, max_length=255, null=True, verbose_name='Частотный диапазон')),
                ('woofer_diameter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Диаметр НЧ-динамика (вуфера)')),
                ('midrange_speaker_diameter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Диаметр СЧ-динамика')),
                ('tweeter_diameter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Диаметр ВЧ-динамика (твитера)')),
                ('speaker_diameter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Диаметр широкополосного динамика')),
                ('body_material', models.CharField(blank=True, max_length=255, null=True, verbose_name='Материал корпуса')),
                ('display', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дисплей')),
                ('voice_assistant', models.CharField(blank=True, max_length=255, null=True, verbose_name='Голосовой ассистент')),
                ('streaming_services', models.CharField(blank=True, max_length=255, null=True, verbose_name='Стриминговые сервисы')),
                ('audio_codec_support', models.CharField(blank=True, max_length=255, null=True, verbose_name='Поддержка аудиокодеков Bluetooth')),
                ('sync', models.CharField(blank=True, max_length=255, null=True, verbose_name='Синхронизация')),
                ('remote_control', models.CharField(blank=True, max_length=255, null=True, verbose_name='Пульт ДУ')),
                ('body_backlight', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подсветка корпуса')),
                ('bluetooth', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bluetooth')),
                ('wifi', models.CharField(blank=True, max_length=255, null=True, verbose_name='Wi-Fi')),
                ('dlna', models.CharField(blank=True, max_length=255, null=True, verbose_name='DLNA')),
                ('usb', models.CharField(blank=True, max_length=255, null=True, verbose_name='USB')),
                ('ethernet', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ethernet')),
                ('battery_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип аккумулятора')),
                ('working_hours', models.CharField(blank=True, max_length=255, null=True, verbose_name='Время работы')),
                ('charging_time', models.CharField(blank=True, max_length=255, null=True, verbose_name='Время зарядки')),
                ('battery_capacity', models.CharField(blank=True, max_length=255, null=True, verbose_name='Емкость аккумулятора')),
                ('width', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ширина')),
                ('depth', models.CharField(blank=True, max_length=255, null=True, verbose_name='Глубина')),
                ('height', models.CharField(blank=True, max_length=255, null=True, verbose_name='Высота')),
                ('weight', models.CharField(blank=True, max_length=255, null=True, verbose_name='Вес')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]