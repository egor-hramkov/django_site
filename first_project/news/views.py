from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect


def index(request):
    return HttpResponse("<h1>Страница с новостями</h1>")

def newsById(request, news_id):
    if news_id > 10:
        return redirect('home')
    return HttpResponse(f"<h1>Страница {news_id} новости<h1>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Данная страница не найдена</h1>')

def home(request):
    return HttpResponse("<h1>Главная страница</h1>")