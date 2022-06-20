from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from .forms import *
from .models import *

menu = [{'title': 'На главную', 'url_name': 'home'}, {'title': 'Новости', 'url_name': 'news'}, {'title': 'Опубликовать новость', 'url_name': 'addNews'}]

def home(request):
    return render(request, 'news/index.html', {'title': 'Главная страница', 'menu': menu})

def news(request):
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
    n = News.objects.filter(id = news_id)
    get_object_or_404(n)
    context = {
        'title': str(news_id) + ' Новость',
        'menu': menu,
        "news": n
    }

    return render(request, 'news/newsById.html', context=context)

def newsByCat(request, cat_slug):
    id_caty = Category.objects.get(slug=cat_slug).id
    c = News.objects.filter(cat_id=id_caty).all()
    get_list_or_404(c)

    context = {
        'title': 'Новости по категории ' + Category.objects.get(id=id_caty).name,
        'menu': menu,
        "news": c
    }
    return render(request, 'news/newsById.html', context=context)

def addNews(request):


    if request.method == 'POST':
        form = AddNewsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                News.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка при добавлении новости')
    else:
        form = AddNewsForm()

    context = {
        'title': 'Добавление новости',
        'menu': menu,
        'form': form
    }
    return render(request, 'news/addNews.html', context=context)

def pageNotFound(request, exception):
    context = {
        'title': 'Страница не найдена',
        'menu': menu,
    }
    return HttpResponseNotFound(render(request, 'news/404.html', context=context))
