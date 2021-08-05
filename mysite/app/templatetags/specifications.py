from django import template
from django.utils.safestring import mark_safe

from ..models import Smartphone
# from app.models import Smartphone

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
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Частота процессора': 'processor_freq',
        'Оперативная карта': 'ram',
        'Видеокарта': 'video',
        'Время работы аккумулятора': 'time_without_charge'
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разрешение экрана': 'resolution',
        'Объем батареи': 'accum_volume',
        'Оперативная память': 'ram',
        'Наличие слота для SD карты': 'sd',
        'Максимальный объем SD карты': 'sd_volume_max',
        'Главная камера (МП)': 'main_cam_mp',
        'Фронтальная камера (МП)': 'frontal_cam_mp'
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
    # if isinstance(product, Smartphone):
    #     if not product.sd:
    #         # PRODUCT_SPEC['smartphone'].pop('Максимальный объем SD карты')
    #         print('product.cd')
    #     else:
    #         PRODUCT_SPEC['smartphone']['Максимальный объем SD карты'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
