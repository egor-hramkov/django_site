from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *

menu = [{'title': 'На главную', 'url_name': 'home'}, {'title': 'Новости', 'url_name': 'news'}, {'title': 'Опубликовать новость', 'url_name': 'addNews'}]

def home(request):
    return render(request, 'news/index.html', {'title': 'Главная страница', 'menu': menu})

class AllNews(ListView):
    model = News
    template_name = "news/news.html"
    context_object_name = 'posts'

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        context['menu'] = menu
        context['cats'] = Category.objects.all()
        context['form'] = SearchNews()
        return context

class NewsByCat(ListView):
    model = News
    template_name = "news/newsByCat.html"
    context_object_name = 'news'

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости по категориям ' + str(self.kwargs['cat_slug'])
        context['menu'] = menu
        return context

    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug']).all()

class newsById(DetailView):
    model = News
    template_name = "news/newsById.html"
    pk_url_kwarg = 'news_id'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(self.kwargs['news_id']) + ' Новость'
        context['menu'] = menu
        return context

class AddNews(CreateView):
    form_class = AddNewsForm
    template_name = 'news/addNews.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление новости"
        context['menu'] = menu
        return context

def pageNotFound(request, exception):
    context = {
        'title': 'Страница не найдена',
        'menu': menu,
    }
    return HttpResponseNotFound(render(request, 'news/404.html', context=context))

def searchNewsBy(request):
    form = SearchNews()
    if request.method == 'POST':
        form = SearchNews(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("searchBy")
        else:
            data=""
        n = News.objects.filter(title__iregex=data).all()
        context = {
            'news': n,
            'form': form,
            'title': 'Новости',
            'menu': menu
        }
        return render(request, 'news/newsBySearch.html', context=context)
    else:
        return redirect('home')

# def news(request):
#     posts = News.objects.all()
#     cats = Category.objects.all()
#     context = {
#         'title': 'Новости',
#         'menu': menu,
#         'posts': posts,
#         'cats': cats
#     }
#     return render(request, 'news/news.html',context=context)

# def newsById(request, news_id):
#     n = News.objects.filter(id = news_id)
#     get_object_or_404(n)
#     context = {
#         'title': str(news_id) + ' Новость',
#         'menu': menu,
#         "news": n
#     }
#     return render(request, 'news/newsById.html', context=context)

# def newsByCat(request, cat_slug):
#     c = News.objects.filter(cat__slug=cat_slug).all()
#
#     context = {
#         'title': 'Новости по категории ' + Category.objects.get(slug=cat_slug).name,
#         'menu': menu,
#         "news": c
#     }
#     return render(request, 'news/newsById.html', context=context)

# def addNews(request):
#     if request.method == 'POST':
#         form = AddNewsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddNewsForm()
#
#     context = {
#         'title': 'Добавление новости',
#         'menu': menu,
#         'form': form
#     }
#     return render(request, 'news/addNews.html', context=context)
