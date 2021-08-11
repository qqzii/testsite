from PIL import Image

from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe

from .models import *


# class NotebookAdminForm(ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].help_text = mark_safe(
#             '<span style="color:red; font-size:14px">При загрузке изображения с разрешением больше {}x{}, '
#             'оно будет обрезано</span>'.format(
#                 *Product.MAX_RESOLUTION
#             )
#         )
#
#     # def clean_image(self):
#     #     image = self.cleaned_data['image']
#     #     img = Image.open(image)
#     #     print(img.width, img.height)
#     #     min_height, min_width = Product.MIN_RESOLUTION
#     #     max_height, max_width = Product.MAX_RESOLUTION
#     #     if image.size > Product.MAX_IMAGE_SIZE:
#     #         raise ValidationError('Размер изображения не должен превышать 5MB')
#     #     if img.height < min_height or img.width < min_width:
#     #         raise ValidationError('Разрешение изображения меньше минимального')
#     #     if img.height > max_height or img.width > max_width:
#     #         raise ValidationError('Разрешение изображения больше максимального')
#     #     return image


class NotebookAdmin(admin.ModelAdmin):

    # form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# class SmartphoneAdminForm(ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         instance = kwargs.get('instance')
#         if not instance.sd:
#             self.fields['sd_volume_max'].widget.attrs.update({
#                 'readonly': True, 'style': 'background: lightgray'
#             })
#
#     def clean(self):
#         if not self.cleaned_data['sd']:
#             self.cleaned_data['sd_volume_max'] = None
#         return self.cleaned_data


class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'admin.html'
    # form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartwatchAdmin(admin.ModelAdmin):

    # form = SmartwatchAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartwatches'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EbookAdmin(admin.ModelAdmin):

    # form = EbookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='ebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TvAdmin(admin.ModelAdmin):

    # form = TvAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='tvs'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MouseAdmin(admin.ModelAdmin):

    # form = MouseAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='mouses'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class KeyboardAdmin(admin.ModelAdmin):

    # form = KeyboardAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='keyboards'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MatAdmin(admin.ModelAdmin):

    # form = MatAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='mats'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)

admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Smartwatch, SmartwatchAdmin)
admin.site.register(Ebook, EbookAdmin)
admin.site.register(Tv, TvAdmin)
admin.site.register(Mouse, MouseAdmin)
admin.site.register(Keyboard, KeyboardAdmin)
admin.site.register(Mat, MatAdmin)

admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
