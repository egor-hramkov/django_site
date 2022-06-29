from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import DataMixin, menu


def home(request):
    return render(request, 'news/index.html', {'title': 'Главная страница', 'menu': menu})

class AllNews(DataMixin, ListView):
    model = News
    template_name = "news/news.html"
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchNews()
        mix_def = self.get_user_context(title='Новости')
        return dict(list(context.items()) + list(mix_def.items()))

class NewsByCat(DataMixin, ListView):
    model = News
    template_name = "news/newsByCat.html"
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title='Новости по категориям ' + str(self.kwargs['cat_slug']))
        return dict(list(context.items()) + list(mix_def.items()))

    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug']).all()

class newsById(DataMixin, DetailView):
    model = News
    template_name = "news/newsById.html"
    pk_url_kwarg = 'news_id'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title=str(self.kwargs['news_id']) + ' Новость')
        return dict(list(context.items()) + list(mix_def.items()))

class AddNews(DataMixin, CreateView):
    form_class = AddNewsForm
    template_name = 'news/addNews.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title="Добавление новости")
        return dict(list(context.items()) + list(mix_def.items()))

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
            request.session['search'] = data
        else:
            data=""
        n = News.objects.filter(title__iregex=data).all()
    else:
        if 'search' in request.session:
            n = News.objects.filter(title__iregex=request.session['search']).all()

    paginator = Paginator(n, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'news': n,
        'form': form,
        'title': 'Новости',
        'menu': menu
    }
    return render(request, 'news/newsBySearch.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('authorize')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(mix_def.items()))

    def form_valid(self, form):
        user = form.save()
        prof = Profile.objects.create(about="", user_id=user.id)
        prof.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(mix_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

class ShowProfile(DataMixin, DetailView):
    model = Profile
    template_name = 'news/profile.html'
    pk_url_kwarg = 'profile_id'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        us_id = Profile.objects.get(id=self.kwargs['profile_id']).user_id
        context['news'] = News.objects.filter(author_id=us_id)
        mix_def = self.get_user_context(title="Профиль пользователя")
        return dict(list(context.items()) + list(mix_def.items()))


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
