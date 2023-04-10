from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http import HttpResponse, FileResponse
import csv

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from .models import Goods, Category
from .forms import GoodsForm, RegisterForm, UserLogin, ContactsForm


def pdf_data(request):
    buf = io.BytesIO()
    can = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    obj = can.beginText()
    obj.setTextOrigin(inch, inch)
    obj.setFont('Helvetica', 14)
    lines = []

    goods = Goods.objects.all()
    for g in goods:
        if not g.discount:
            g.discount = '-'
        lines.append(str(g.name))
        lines.append(str(g.price))
        lines.append(str(g.discount))
        lines.append(str(g.id))
        lines.append(" ")

    for line in lines:
        obj.textLine(line)

    can.drawText(obj)
    can.showPage()
    can.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='товары.pdf')


def csv_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=товары.csv'
    response.write(u'\ufeff'.encode('utf8'))  # response["Content-Encoding"] = 'UTF-8'
    writer = csv.writer(response)
    goods = Goods.objects.all()
    writer.writerow(['Наименование товара', 'Цена', 'Цена со скидкой', 'Категория товара', 'id товара'])
    for g in goods:
        writer.writerow([g.name, g.price, g.discount, g.category, g.id])
    return response


def txt_data(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=товары.txt'
    goods = Goods.objects.all()
    lines = []
    for g in goods:
        if not g.discount:
            g.discount = '-'
        lines.append(f"{g.name}\n {g.price}\n {g.discount}\n {g.category}\n {g.id}\n\n\n")
    response.writelines(lines)
    return response


class HomeGoods(ListView):
    model = Goods
    template_name = 'goods/index.html'
    context_object_name = 'goods'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeGoods, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Goods.objects.filter(is_published=True)


# def index(request):
#     goods = Goods.objects.all()
#     context = {
#         'goods': goods,
#     }
#     return render(request, template_name='goods/index.html', context=context)


class CategoryGoods(ListView):
    model = Category
    template_name = 'goods/index.html'
    context_object_name = 'goods'
    allow_empty = False
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryGoods, self).get_context_data(**kwargs)
        cats = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = cats
        # context['subcat'] = cats.filter
        return context

    def get_queryset(self):
        return Goods.objects.filter(category_id=self.kwargs['category_id'], is_published=True)


# def get_category(request, category_id):
#     goods = Goods.objects.filter(category_id=category_id)
#     current_category = Category.objects.get(pk=category_id)
#     context = {
#         'goods': goods,
#         'current_category': current_category,
#     }
#     return render(request, template_name='goods/category.html', context=context)

class DetailGoods(DetailView):
    model = Goods
    template_name = 'goods/goods.html'
    context_object_name = 'goods'

    pk_url_kwarg = 'goods_id'


# def get_goods(request, goods_id):
#     # goods = Goods.objects.get(pk=goods_id)
#     goods = get_object_or_404(Goods, pk=goods_id)
#     context = {
#         'goods': goods,
#     }
#     return render(request, template_name='goods/goods.html', context=context)


class CreateGoods(LoginRequiredMixin, CreateView):
    form_class = GoodsForm
    template_name = 'goods/add-goods.html'
    # success_url = reverse_lazy('home')
    redirect_field_name = reverse_lazy('home')


class UpdateGoods(LoginRequiredMixin, UpdateView):
    form_class = GoodsForm
    template_name = 'goods/update-goods.html'
    redirect_field_name = reverse_lazy('update-goods')
    pk_url_kwarg = 'goods_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UpdateGoods, self).get_context_data(**kwargs)
        good = Goods.objects.get(pk=self.kwargs['goods_id'])
        context['good'] = good
        return context

    def get_queryset(self):
        return Goods.objects.filter(pk=self.kwargs['goods_id'], is_published=True)


# def add_goods(request):
#     if request.method == 'POST':
#         form = GoodsForm(request.POST)
#         if form.is_valid():
#             # Goods.gobjects.create(**form.cleaned_data)
#             goods = form.save()
#             return redirect(goods)
#     else:
#         form = GoodsForm()
#     return render(request, 'goods/add-goods.html', {'form': form})

def example(request):
    objects = [i for i in range(20)]
    paginator = Paginator(objects, 5)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'goods/example.html', {'page_obj': page_objects})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации.')
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'goods/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLogin()
    context = {
        'form': form,
    }

    return render(request, 'goods/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def send_message(request):
    if request.method == 'POST':
        form = ContactsForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'never_f0rget@bk.ru',
                             ['ydtalel@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено.')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка отправки.')

        else:
            messages.error(request, 'Ошибка валидации.')
    else:
        form = ContactsForm()
    context = {
        'form': form,
    }
    return render(request, 'goods/email.html', context)


class SearchGoods(ListView):
    model = Goods
    template_name = 'goods/search.html'
    context_object_name = 'goods'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchGoods, self).get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        return context

    def get_queryset(self):
        return Goods.objects.filter(name__icontains=self.request.GET.get('search'))
