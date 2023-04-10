from django import template

from goods.models import Category, Goods

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_goods():
    return Goods.objects.all()


@register.inclusion_tag('goods/categories_inc_tags.html')
def show_categories():
    categories = Category.objects.all()
    return {'cat': categories}
