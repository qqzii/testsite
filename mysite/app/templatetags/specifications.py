from django import template
from django.utils.safestring import mark_safe


register = template.Library()

TABLE_HEAD = """
                <table class="product-main__table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr class="product-main__row">
                      <td class="product-main__col">{name}</td>
                      <td class="product-main__col">{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'notebook': {
        'Дата выхода на рынок': 'market_date',
        'Продуктовая линейка': 'product_line',
        'Тип': 'type',
        'Назначение': 'appointment',
        'Процессор': 'cpu',
        'Модель процессора': 'model_cpu',
        'Количество ядер': 'number_of_cores',
        'Количество потоков': 'number_of_threads',
        'Тактовая частота': 'clock_frequency',
        'Turbo-частота': 'turbo_frequency',
        'Энергопотребление процессора': 'cpu_power_consumption',
        'Встроенная в процессор графика': 'processor_graphics',
        'Материал корпуса': 'body_material',
        'Цвет корпуса': 'body_color',
        'Материал крышки': 'cover_material',
        'Цвет крышки': 'cover_color',
        'Подсветка корпуса': 'body_backlight',
        'Защищенный корпус': 'body_protected',
        'Ширина': 'width',
        'Глубина': 'depth',
        'Толщина': 'thickness',
        'Вес': 'weight',
        'Диагональ экрана': 'screen_diagonal',
        'Разрешение экрана': 'screen_resolution',
        'Частота матрицы': 'matrix_frequency',
        'Технология экрана': 'screen_technology',
        'Яркость экрана': 'screen_brightness',
        'Поверхность экрана': 'screen_surface',
        'Экран': 'screen',
        'Тип оперативной памяти': 'ram_type',
        'Частота оперативной памяти': 'ram_frequency',
        'Объём памяти': 'ram_volume',
        'Максимальный объём памяти': 'max_ram_volume',
        'Всего слотов памяти': 'total_memory_slots',
        'Свободных слотов памяти': 'free_memory_slots',
        'Конфигурация накопителя': 'drive_configuration',
        'Тип накопителя': 'drive_type',
        'Ёмкость накопителя': 'drive_volume',
        'Модель видеокарты': 'graphics_card_model',
        'Локальная видеопамять': 'local_video_memory',
        'Камера': 'camera',
        'Основная камера': 'main_cam',
        'Встроенный микрофон': 'microphone',
        'Встроенные динамики': 'speakers',
        'Цифровое поле': 'digital_field',
        'Управление курсором': 'cursor_control',
        'NFC': 'nfc',
        'Bluetooth': 'bluetooth',
        'LAN': 'lan',
        'Wi-Fi': 'wifi',
        'Всего USB Type A': 'usb_type_a',
        'USB 2.0': 'usb_2',
        'USB 3.2 Gen1 Type-A': 'usb_32_gen1_a',
        'USB 3.2 Gen2 Type-A': 'usb_32_gen2_a',
        'Всего USB Type C': 'usb_type_c',
        'USB 3.2 Gen1 Type-C': 'usb_32_gen1_c',
        'USB 3.2 Gen2 Type-C': 'usb_32_gen2_c',
        'USB 3.2 Gen 2x2': 'usb_32_gen2x2',
        'USB4': 'usb4',
        'Максимальная скорость передачи данных USB': 'maximum_baud_rate_usb',
        'HDMI': 'hdmi',
        'Аудио выходы': 'audio_outputs',
        'Запас энергии': 'energy_reserve',
        'Время работы': 'working_hours',
        'Зарядка ноутбука через USB Type-C': 'charge_via_type_c',
        'Адаптер питания USB-C': 'power_adapter_usb_c',
        'Быстрая зарядка': 'fast_charging',
        'Операционная система': 'operating_system'
    },
    'smartphone': {
        'Дата выхода на рынок': 'market_date',
        'Тип': 'type',
        'Операционная система': 'operating_system',
        'Версия операционной системы': 'version_operating_system',
        'Размер экрана': 'screen_size',
        'Разрешение экрана': 'screen_resolution',
        'Оперативная память': 'ram',
        'Флэш-память': 'flash_memory',
        'Количество основных камер': 'number_of_main_cameras',
        'Количество точек матрицы': 'number_of_matrix_points',
        'Количество SIM-карт': 'number_of_sim',
        'Формат SIM-карты': 'format_of_sim',
        'Максимальное разрешение видео': 'max_video_resolution',
        'Поддержка карт памяти': 'memory_card_support',
        'Платформа': 'platform',
        'Процессор': 'cpu',
        'Тактовая частота процессора': 'clock_frequency_cpu',
        'Количество ядер': 'number_of_cores',
        'Разрядность процессора': 'cpu_size',
        'Техпроцесс': 'technical_process',
        'Графический ускоритель': 'graphics_accelerator',
        'Частота ГПУ': 'gpu_frequency',
        'Конструкция корпуса': 'body_design',
        'Материал корпуса': 'body_material',
        'Материал задней крышки': 'back_cover_material',
        'Цвет корпуса': 'body_color',
        'Цвет фронтальной панели': 'front_cover_color',
        'Расположение фронтальной камеры': 'front_camera_location',
        'Расположение сканера отпечатка пальца': 'fingerprint_reader_location',
        'Ширина': 'width',
        'Глубина': 'depth',
        'Толщина': 'thickness',
        'Вес': 'weight',
        'Технология экрана': 'screen_technology',
        'Количество цветов экрана': 'number_of_screen_colors',
        'Разрешающая способность экрана': 'screen_ability_resolution',
        'Соотношение сторон': 'aspect_ratio',
        'Частота обновления экрана': 'screen_refresh_rate',
        'Сенсорный экран': 'touch_screen',
        'Защита от царапин': 'scratch_protection',
        'Встроенная вспышка': 'built_in_flash',
        'Автоматическая фокусировка': 'auto_focus',
        'Оптическая стабилизация': 'optical_stabilization',
        'Максимальное количество кадров в секунду': 'max_fps',
        'Фронтальная камера': 'front_camera',
        'Стереодинамики': 'stereo_speakers',
        'Сканер отпечатка пальца': 'fingerprint_reader',
        'Разблокировка по лицу': 'face_unlock',
        'ИК-передатчик': 'ir_transmitter',
        'FM-приёмник': 'fm_receiver',
        'Беспроводная зарядка': 'wireless_charger',
        'Быстрая зарядка': 'fast_charging',
        'Акселерометр': 'accelerometer',
        'Гироскоп': 'gyroscope',
        'Датчик освещенности': 'light_sensor',
        'Барометр': 'barometer',
        'ANT+': 'ant',
        'GPS': 'gps',
        'ГЛОНАСС': 'glonass',
        'Beidou': 'beidou',
        'EDGE': 'edge',
        'HSPA': 'hspa',
        'HSPA+': 'hspa_plus',
        'LTE': 'lte',
        '5G': 'g5',
        'Bluetooth': 'bluetooth',
        'Аудиовыход': 'audio_output',
        'Wi-Fi': 'wifi',
        'Разъём подключения': 'connection_socket',
        'NFC': 'nfc',
        'Тип аккумулятора': 'battery_type',
        'Емкость аккумулятора': 'battery_capacity'
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
