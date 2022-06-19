from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = [{'title': 'На главную', 'url_name': 'home'}, {'title': 'Новости', 'url_name': 'news'}]

def home(request):
    return render(request, 'news/index.html', {'title': 'Главная страница', 'menu': menu})

def index(request):
    posts = News.objects.all()
    cats = Category.objects.all()
    context = {
        'title': 'Новости',
        'menu': menu,
        'posts': posts,
        'cats': cats
    }
    return render(request, 'news/news.html',context=context)

def newsById(request, news_id):
    if news_id < 1:
        raise Http404()
    n = News.objects.filter(id = news_id)
    context = {
        'title': str(news_id) + ' Новость',
        'menu': menu,
        "news": n
    }

    return render(request, 'news/newsById.html', context=context)

def newsByCat(request, cat_id):
    if cat_id < 1:
        raise Http404()
    c = News.objects.filter(cat_id = cat_id).all()

    context = {
        'title': 'Новости по категории ' + Category.objects.get(id=cat_id).name,
        'menu': menu,
        "news": c
    }
    return render(request, 'news/newsById.html', context=context)

def pageNotFound(request, exception):
    context = {
        'title': 'Страница не найдена',
        'menu': menu,
    }
    return HttpResponseNotFound(render(request, 'news/404.html', context=context))
