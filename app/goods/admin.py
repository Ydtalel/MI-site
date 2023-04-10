from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Category, Goods


class GoodsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Goods
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name')
    list_filter = ('name',)
    list_display_links = ('name',)

    search_fields = ('name', 'id',)


class GoodsAdmin(admin.ModelAdmin):
    form = GoodsAdminForm
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    list_display = ('id', 'name', 'slug', 'price', 'discount', 'category', 'subcategory',
                    'is_published', 'get_mini_photo')
    list_display_links = ('id', 'name')
    list_editable = ['is_published', ]
    list_filter = ('category', 'subcategory', 'price', 'discount')
    search_fields = ('name', 'category', 'subcategory', 'price', 'discount',)
    readonly_fields = ('created', 'updated', 'views', 'get_mini_photo')
    fields = ('name', 'slug', 'category', 'subcategory', 'content', 'price', 'discount', 'photo',
              'get_mini_photo', 'video', 'views', 'created', 'updated', 'is_published',)

    def get_mini_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}'width='75'>")

    get_mini_photo.short_description = 'Фото'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goods, GoodsAdmin)

admin.site.site_title = 'Управление Товарами'
admin.site.site_header = 'Управление Товарами'
