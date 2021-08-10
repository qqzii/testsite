import sys
from PIL import Image

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone

from io import BytesIO

User = get_user_model()

# 1 категории
# 2 товар
# 3 товар в корзине
# 4 корзина
# 5 заказ
# 6 покупатель
# 7 спецификации


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфоны': 'smartphone__count',
        'Умные часы': 'smartwatch__count',
        'Электронные книги': 'ebook__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_category_menu(self):
        models = get_models_for_count('notebook', 'smartphone', 'smartwatch', 'ebook')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Название категории')
    image = models.ImageField(verbose_name='Изображение', null=True)
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    # MIN_RESOLUTION = (400, 400)
    # MAX_RESOLUTION = (400, 600)
    # RESIZE_RESOLUTION = (200, 200)
    # MAX_IMAGE_SIZE = 5242880

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(null=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    # def save(self, *args, **kwargs):
    #     image = self.image
    #     img = Image.open(image)
    #     # min_height, min_width = self.MIN_RESOLUTION
    #     # max_height, max_width = self.MAX_RESOLUTION
    #     # if img.height < min_height or img.width < min_width:
    #     #     raise MinResolutionErrorException('Разрешение изображения меньше минимального')
    #     # if img.height > max_height or img.width > max_width:
    #     #     raise MaxResolutionErrorException('Разрешение изображения больше максимального')
    #     new_img = img.convert('RGB')
    #     resized_new_img = new_img.resize(self.RESIZE_RESOLUTION, Image.ANTIALIAS)
    #     filestream = BytesIO()
    #     resized_new_img.save(filestream, 'JPEG', quality=90)
    #     filestream.seek(0)
    #     name = '{}.{}'.format(*self.image.name.split('.'))
    #     self.image = InMemoryUploadedFile(
    #         filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
    #     )
    #     super().save(*args, **kwargs)


class Notebook(Product):

    market_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дата выхода на рынок')
    product_line = models.CharField(max_length=255, null=True, blank=True, verbose_name='Продуктовая линейка')
    type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип')
    appointment = models.CharField(max_length=255, null=True, blank=True, verbose_name='Назначение')
    cpu = models.CharField(max_length=255, null=True, blank=True, verbose_name='Процессор')
    model_cpu = models.CharField(max_length=255, null=True, blank=True, verbose_name='Модель процессора')
    number_of_cores = models.CharField(max_length=255, null=True, blank=True, verbose_name='Количество ядер')
    number_of_threads = models.CharField(max_length=255, null=True, blank=True, verbose_name='Количество потоков')
    clock_frequency = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тактовая частота')
    turbo_frequency = models.CharField(max_length=255, null=True, blank=True, verbose_name='Turbo-частота')
    cpu_power_consumption = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Энергопотребление процессора'
    )
    processor_graphics = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Встроенная в процессор графика'
    )
    body_material = models.CharField(max_length=255, null=True, blank=True, verbose_name='Материал корпуса')
    body_color = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цвет корпуса')
    cover_material = models.CharField(max_length=255, null=True, blank=True, verbose_name='Материал крышки')
    cover_color = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цвет крышки')
    body_backlight = models.CharField(max_length=255, null=True, blank=True, verbose_name='Подсветка корпуса')
    body_protected = models.CharField(max_length=255, null=True, blank=True, verbose_name='Защищенный корпус')
    width = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ширина')
    depth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Глубина')
    thickness = models.CharField(max_length=255, null=True, blank=True, verbose_name='Толщина')
    weight = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вес')
    screen_diagonal = models.CharField(max_length=255, null=True, blank=True, verbose_name='Диагональ экрана')
    screen_resolution = models.CharField(max_length=255, null=True, blank=True, verbose_name='Разрешение экрана')
    matrix_frequency = models.CharField(max_length=255, null=True, blank=True, verbose_name='Частота матрицы')
    screen_technology = models.CharField(max_length=255, null=True, blank=True, verbose_name='Технология экрана')
    screen_brightness = models.CharField(max_length=255, null=True, blank=True, verbose_name='Яркость экрана')
    screen_surface = models.CharField(max_length=255, null=True, blank=True, verbose_name='Поверхность экрана')
    screen = models.CharField(max_length=255, null=True, blank=True, verbose_name='Экран')
    ram_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип оперативной памяти')
    ram_frequency = models.CharField(max_length=255, null=True, blank=True, verbose_name='Частота оперативной памяти')
    ram_volume = models.CharField(max_length=255, null=True, blank=True, verbose_name='Объём памяти')
    max_ram_volume = models.CharField(max_length=255, null=True, blank=True, verbose_name='Максимальный объём памяти')
    total_memory_slots = models.CharField(max_length=255, null=True, blank=True, verbose_name='Всего слотов памяти')
    free_memory_slots = models.CharField(max_length=255, null=True, blank=True, verbose_name='Свободных слотов памяти')
    drive_configuration = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Конфигурация накопителя'
    )
    drive_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип накопителя')
    drive_volume = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ёмкость накопителя')
    graphics_card_model = models.CharField(max_length=255, null=True, blank=True, verbose_name='Модель видеокарты')
    local_video_memory = models.CharField(max_length=255, null=True, blank=True, verbose_name='Локальная видеопамять')
    camera = models.CharField(max_length=255, null=True, blank=True, verbose_name='Камера')
    main_cam = models.CharField(max_length=255, null=True, blank=True, verbose_name='Основная камера')
    microphone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Встроенный микрофон')
    speakers = models.CharField(max_length=255, null=True, blank=True, verbose_name='Встроенные динамики')
    digital_field = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цифровое поле')
    cursor_control = models.CharField(max_length=255, null=True, blank=True, verbose_name='Управление курсором')
    nfc = models.CharField(max_length=255, null=True, blank=True, verbose_name='NFC')
    bluetooth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bluetooth')
    lan = models.CharField(max_length=255, null=True, blank=True, verbose_name='LAN')
    wifi = models.CharField(max_length=255, null=True, blank=True, verbose_name='Wi-Fi')
    usb_type_a = models.CharField(max_length=255, null=True, blank=True, verbose_name='Всего USB Type A')
    usb_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB 2.0')
    usb_32_gen1_a = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB 3.2 Gen1 Type-A')
    usb_32_gen2_a = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB 3.2 Gen2 Type-A')
    usb_type_c = models.CharField(max_length=255, null=True, blank=True, verbose_name='Всего USB Type C')
    usb_32_gen1_c = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB 3.2 Gen1 Type-C')
    usb_32_gen2_c = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB 3.2 Gen2 Type-C')
    usb_32_gen2x2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB 3.2 Gen 2x2')
    usb4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB4')
    maximum_baud_rate_usb = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальная скорость передачи данных USB'
    )
    hdmi = models.CharField(max_length=255, null=True, blank=True, verbose_name='HDMI')
    audio_outputs = models.CharField(max_length=255, null=True, blank=True, verbose_name='Аудио выходы')
    energy_reserve = models.CharField(max_length=255, null=True, blank=True, verbose_name='Запас энергии')
    working_hours = models.CharField(max_length=255, null=True, blank=True, verbose_name='Время работы')
    charge_via_type_c = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Зарядка ноутбука через USB Type-C'
    )
    power_adapter_usb_c = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адаптер питания USB-C')
    fast_charging = models.CharField(max_length=255, null=True, blank=True, verbose_name='Быстрая зарядка')
    operating_system = models.CharField(max_length=255, null=True, blank=True, verbose_name='Операционная система')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):

    market_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дата выхода на рынок')
    type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип')
    operating_system = models.CharField(max_length=255, null=True, blank=True, verbose_name='Операционная система')
    version_operating_system = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Версия операционной системы'
    )
    screen_size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Размер экрана')
    screen_resolution = models.CharField(max_length=255, null=True, blank=True, verbose_name='Разрешение экрана')
    ram = models.CharField(max_length=255, null=True, blank=True, verbose_name='Оперативная память')
    flash_memory = models.CharField(max_length=255, null=True, blank=True, verbose_name='Флэш-память')
    number_of_main_cameras = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Количество основных камер'
    )
    number_of_matrix_points = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Количество точек матрицы'
    )
    number_of_sim = models.CharField(max_length=255, null=True, blank=True, verbose_name='Количество SIM-карт')
    format_of_sim = models.CharField(max_length=255, null=True, blank=True, verbose_name='Формат SIM-карты')
    max_video_resolution = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальное разрешение видео'
    )
    memory_card_support = models.CharField(max_length=255, null=True, blank=True, verbose_name='Поддержка карт памяти')
    platform = models.CharField(max_length=255, null=True, blank=True, verbose_name='Платформа')
    cpu = models.CharField(max_length=255, null=True, blank=True, verbose_name='Процессор')
    clock_frequency_cpu = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Тактовая частота процессора'
    )
    number_of_cores = models.CharField(max_length=255, null=True, blank=True, verbose_name='Количество ядер')
    cpu_size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Разрядность процессора')
    technical_process = models.CharField(max_length=255, null=True, blank=True, verbose_name='Техпроцесс')
    graphics_accelerator = models.CharField(max_length=255, null=True, blank=True, verbose_name='Графический ускоритель')
    gpu_frequency = models.CharField(max_length=255, null=True, blank=True, verbose_name='Частота ГПУ')
    body_design = models.CharField(max_length=255, null=True, blank=True, verbose_name='Конструкция корпуса')
    body_material = models.CharField(max_length=255, null=True, blank=True, verbose_name='Материал корпуса')
    back_cover_material = models.CharField(max_length=255, null=True, blank=True, verbose_name='Материал задней крышки')
    body_color = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цвет корпуса')
    front_cover_color = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цвет фронтальной панели')
    front_camera_location = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Расположение фронтальной камеры'
    )
    fingerprint_reader_location = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Расположение сканера отпечатка пальца'
    )
    width = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ширина')
    depth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Глубина')
    thickness = models.CharField(max_length=255, null=True, blank=True, verbose_name='Толщина')
    weight = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вес')
    screen_technology = models.CharField(max_length=255, null=True, blank=True, verbose_name='Технология экрана')
    number_of_screen_colors = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Количество цветов экрана'
    )
    screen_ability_resolution = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Разрешающая способность экрана'
    )
    aspect_ratio = models.CharField(max_length=255, null=True, blank=True, verbose_name='Соотношение сторон')
    screen_refresh_rate = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Частота обновления экрана'
    )
    touch_screen = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сенсорный экран')
    scratch_protection = models.CharField(max_length=255, null=True, blank=True, verbose_name='Защита от царапин')
    built_in_flash = models.CharField(max_length=255, null=True, blank=True, verbose_name='Встроенная вспышка')
    auto_focus = models.CharField(max_length=255, null=True, blank=True, verbose_name='Автоматическая фокусировка')
    optical_stabilization = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Оптическая стабилизация'
    )
    max_fps = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальное количество кадров в секунду'
    )
    front_camera = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фронтальная камера')
    stereo_speakers = models.CharField(max_length=255, null=True, blank=True, verbose_name='Стереодинамики')
    fingerprint_reader = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сканер отпечатка пальца')
    face_unlock = models.CharField(max_length=255, null=True, blank=True, verbose_name='Разблокировка по лицу')
    ir_transmitter = models.CharField(max_length=255, null=True, blank=True, verbose_name='ИК-передатчик')
    fm_receiver = models.CharField(max_length=255, null=True, blank=True, verbose_name='FM-приёмник')
    wireless_charger = models.CharField(max_length=255, null=True, blank=True, verbose_name='Беспроводная зарядка')
    fast_charging = models.CharField(max_length=255, null=True, blank=True, verbose_name='Быстрая зарядка')
    accelerometer = models.CharField(max_length=255, null=True, blank=True, verbose_name='Акселерометр')
    gyroscope = models.CharField(max_length=255, null=True, blank=True, verbose_name='Гироскоп')
    light_sensor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Датчик освещенности')
    barometer = models.CharField(max_length=255, null=True, blank=True, verbose_name='Барометр')
    ant = models.CharField(max_length=255, null=True, blank=True, verbose_name='ANT+')
    gps = models.CharField(max_length=255, null=True, blank=True, verbose_name='GPS')
    glonass = models.CharField(max_length=255, null=True, blank=True, verbose_name='ГЛОНАСС')
    beidou = models.CharField(max_length=255, null=True, blank=True, verbose_name='Beidou')
    edge = models.CharField(max_length=255, null=True, blank=True, verbose_name='EDGE')
    hspa = models.CharField(max_length=255, null=True, blank=True, verbose_name='HSPA')
    hspa_plus = models.CharField(max_length=255, null=True, blank=True, verbose_name='HSPA+')
    lte = models.CharField(max_length=255, null=True, blank=True, verbose_name='LTE')
    g5 = models.CharField(max_length=255, null=True, blank=True, verbose_name='5G')
    bluetooth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bluetooth')
    audio_output = models.CharField(max_length=255, null=True, blank=True, verbose_name='Аудиовыход')
    wifi = models.CharField(max_length=255, null=True, blank=True, verbose_name='Wi-Fi')
    connection_socket = models.CharField(max_length=255, null=True, blank=True, verbose_name='Разъём подключения')
    nfc = models.CharField(max_length=255, null=True, blank=True, verbose_name='NFC')
    battery_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип аккумулятора')
    battery_capacity = models.CharField(max_length=255, null=True, blank=True, verbose_name='Емкость аккумулятора')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartwatch(Product):

    market_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дата выхода на рынок')
    flash_memory = models.CharField(max_length=255, null=True, blank=True, verbose_name='Флэш-память')
    built_in_camera = models.CharField(max_length=255, null=True, blank=True, verbose_name='Встроенная камера')
    type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип')
    platform_support = models.CharField(max_length=255, null=True, blank=True, verbose_name='Поддержка платформ')
    body_material = models.CharField(max_length=255, null=True, blank=True, verbose_name='Материал корпуса')
    body_color = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цвет корпуса')
    built_in_music_player = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Встроенный музыкальный плеер'
    )
    calls = models.CharField(max_length=255, null=True, blank=True, verbose_name='Звонки')
    voice_control = models.CharField(max_length=255, null=True, blank=True, verbose_name='Голосовое управление')
    remote_control = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дистанционное управление')
    contactless_payments = models.CharField(max_length=255, null=True, blank=True, verbose_name='Бесконтактные платежи')
    vibration = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вибрация')
    width = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ширина')
    depth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Глубина')
    thickness = models.CharField(max_length=255, null=True, blank=True, verbose_name='Толщина')
    weight = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вес')
    bracelet_size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Размеры браслета')
    screen_technology = models.CharField(max_length=255, null=True, blank=True, verbose_name='Технология экрана')
    number_of_screen_colors = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Количество цветов экрана'
    )
    screen_size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Размер экрана')
    screen_resolution = models.CharField(max_length=255, null=True, blank=True, verbose_name='Разрешение экрана')
    screen_ability_resolution = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Разрешающая способность экрана'
    )
    touch_screen = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сенсорный экран')
    scratch_protection = models.CharField(max_length=255, null=True, blank=True, verbose_name='Защита от царапин')
    accelerometer = models.CharField(max_length=255, null=True, blank=True, verbose_name='Акселерометр')
    gyroscope = models.CharField(max_length=255, null=True, blank=True, verbose_name='Гироскоп')
    light_sensor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Датчик освещенности')
    barometer = models.CharField(max_length=255, null=True, blank=True, verbose_name='Барометр')
    pedometer = models.CharField(max_length=255, null=True, blank=True, verbose_name='Шагомер')
    heart_rate = models.CharField(max_length=255, null=True, blank=True, verbose_name='Пульсометр')
    ecg_sensor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Датчик ЭКГ')
    compass = models.CharField(max_length=255, null=True, blank=True, verbose_name='Компас')
    depth_gauge = models.CharField(max_length=255, null=True, blank=True, verbose_name='Глубиномер')
    gps = models.CharField(max_length=255, null=True, blank=True, verbose_name='GPS')
    glonass = models.CharField(max_length=255, null=True, blank=True, verbose_name='ГЛОНАСС')
    bluetooth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bluetooth')
    audio_output = models.CharField(max_length=255, null=True, blank=True, verbose_name='Аудиовыход')
    wifi = models.CharField(max_length=255, null=True, blank=True, verbose_name='Wi-Fi')
    usb = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB')
    nfc = models.CharField(max_length=255, null=True, blank=True, verbose_name='NFC')
    battery_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип аккумулятора')
    battery_capacity = models.CharField(max_length=255, null=True, blank=True, verbose_name='Емкость аккумулятора')
    working_hours = models.CharField(max_length=255, null=True, blank=True, verbose_name='Время работы')
    wireless_charger = models.CharField(max_length=255, null=True, blank=True, verbose_name='Беспроводная зарядка')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Ebook(Product):

    market_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дата выхода на рынок')
    screen_size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Размер экрана')
    screen_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип экрана')
    screen_technology = models.CharField(max_length=255, null=True, blank=True, verbose_name='Технология экрана')
    screen_resolution = models.CharField(max_length=255, null=True, blank=True, verbose_name='Разрешение экрана')
    os_version = models.CharField(max_length=255, null=True, blank=True, verbose_name='Версия операционной системы')
    ram = models.CharField(max_length=255, null=True, blank=True, verbose_name='Оперативная память')
    flash_memory = models.CharField(max_length=255, null=True, blank=True, verbose_name='Флэш-память')
    built_in_camera = models.CharField(max_length=255, null=True, blank=True, verbose_name='Встроенная камера')
    body_material = models.CharField(max_length=255, null=True, blank=True, verbose_name='Материал корпуса')
    body_color = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цвет корпуса')
    width = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ширина')
    length = models.CharField(max_length=255, null=True, blank=True, verbose_name='Длина')
    thickness = models.CharField(max_length=255, null=True, blank=True, verbose_name='Толщина')
    weight = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вес')
    touch_screen = models.CharField(max_length=255, null=True, blank=True, verbose_name='Сенсорный экран')
    screen_backlight = models.CharField(max_length=255, null=True, blank=True, verbose_name='Подсветка экрана')
    support_txt_format = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Поддержка текстовых форматов'
    )
    support_photo_format = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Поддержка фото форматов'
    )
    support_audio_format = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Поддержка аудио форматов'
    )
    support_archive = models.CharField(max_length=255, null=True, blank=True, verbose_name='Поддержка архивов')
    support_video_format = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Поддержка видео форматов'
    )
    memory_card_support = models.CharField(max_length=255, null=True, blank=True, verbose_name='Поддержка карт памяти')
    sound_recording = models.CharField(max_length=255, null=True, blank=True, verbose_name='Запись звука')
    built_in_speaker = models.CharField(max_length=255, null=True, blank=True, verbose_name='Встроенный динамик')
    built_in_microphone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Встроенный микрофон')
    bluetooth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bluetooth')
    audio_output = models.CharField(max_length=255, null=True, blank=True, verbose_name='Аудиовыход')
    wifi = models.CharField(max_length=255, null=True, blank=True, verbose_name='Wi-Fi')
    modem_3g = models.CharField(max_length=255, null=True, blank=True, verbose_name='3G-модем')
    usb = models.CharField(max_length=255, null=True, blank=True, verbose_name='USB')
    battery_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Тип аккумулятора')
    battery_capacity = models.CharField(max_length=255, null=True, blank=True, verbose_name='Емкость аккумулятора')
    battery_life = models.CharField(max_length=255, null=True, blank=True, verbose_name='Время автономной работы')
    charging_time = models.CharField(max_length=255, null=True, blank=True, verbose_name='Время зарядки')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер пользователя', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(
        Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE
    )
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)


# class Specification(models.Model):
#
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     name = models.CharField(max_length=255, verbose_name='Имя товара для характеристик')
#
#     def __str__(self):
#         return 'Характеристики для товара {}'.format(self.name)

