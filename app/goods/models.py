from django.db import models
from django.urls import reverse
import uuid


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Заголовок категории')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})


class Goods(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование товара')
    content = models.TextField(blank=True, verbose_name='Характеристики товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='Цена со скидкой',
                                   null=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL товара')
    subcategory = models.CharField(max_length=100, verbose_name='Подкатегория')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    video = models.FileField(upload_to='videos/%Y/%m/%d/', blank=True, verbose_name='Видео')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    is_published = models.BooleanField(verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='goods', verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-price', 'name']

    def get_absolute_url(self):
        return reverse('goods', kwargs={'goods_id': self.pk})



# class OU(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     parent = models.ForeignKey('self', related_name='subordinate', on_delete=models.DO_NOTHING, db_constraint=False)  # ,blank=True, null=True) # как раз это поле реализует связь с родителем
#     Name = models.CharField(max_length=200)
#     Description = models.TextField(blank=True, null=True)