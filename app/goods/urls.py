from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('', index, name='home'),
    path('', HomeGoods.as_view(), name='home'),  # extra_context={'title': 'Главная'}
    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', CategoryGoods.as_view(), name='category'),

    # path('goods/<int:goods_id>/', get_goods, name='goods'),
    path('goods/<int:goods_id>/', DetailGoods.as_view(), name='goods'),
    # path('goods/add-goods/', add_goods, name='add-goods'),
    path('goods/add-goods/', CreateGoods.as_view(), name='add-goods'),
    path('goods/<int:goods_id>/update-goods/', UpdateGoods.as_view(), name='update-goods'),
    path('contact/', send_message, name='contact'),
    path('search/', SearchGoods.as_view(), name='search'),
    path('txt_data', txt_data, name='txt'),
    path('csv_data', csv_data, name='csv'),
    path('pdf_data', pdf_data, name='pdf'),
]
