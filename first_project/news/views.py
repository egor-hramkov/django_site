from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .models import *

menu = ['Войти', 'Добавить новость', 'О сайте']

def index(request):
    posts = News.objects.all()
    return render(request, 'news/news.html', {'title': 'Новости', 'menu': menu, 'posts': posts})

def newsById(request, news_id):
    if news_id < 1:
        return redirect('home')
    return render(request, 'news/news_byId.html', {'title': str(news_id) + ' Новость', 'menu': menu})

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Данная страница не найдена</h1>')

def home(request):
    return render(request, 'news/index.html', {'title': 'Главная страница', 'menu': menu})