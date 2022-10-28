import json
import os.path
import smtplib

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, FormView

from account.models import Profile
from .forms import *
from .models import *
from .utils import DataMixin

import uuid
from itertools import chain
import smtplib
from email.mime.text import MIMEText
import configparser

def home(request):
    return render(request, 'news/index.html', {'title': 'Главная страница'})

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

    def get_queryset(self):
        return News.objects.select_related('cat', 'author', 'author__profile').all()

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
        return News.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat', 'author', 'author__profile')

class newsById(DataMixin, DetailView):
    model = News
    template_name = "news/newsById.html"
    pk_url_kwarg = 'news_id'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title=str(self.kwargs['news_id']) + ' Новость')
        return dict(list(context.items()) + list(mix_def.items()))

class AddNews(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddNewsForm
    template_name = 'news/addNews.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title="Добавление новости")
        return dict(list(context.items()) + list(mix_def.items()))

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.author = User.objects.get(id=self.request.user.id)
        fields.save()
        return super().form_valid(form)

def pageNotFound(request, exception):
    context = {
        'title': 'Страница не найдена',
    }
    return HttpResponseNotFound(render(request, 'news/404.html', context=context))

@cache_page(60)
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

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(RegisterUser, self).dispatch(request, *args, **kwargs)

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


class AllUsers(DataMixin, ListView):
    model = User
    template_name = "news/allUsers.html"
    context_object_name = 'users'
    paginate_by = 3

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchNews
        mix_def = self.get_user_context(title='Список пользователей')
        return dict(list(context.items()) + list(mix_def.items()))

    def get_queryset(self):
        return User.objects.select_related('profile').all()

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'news/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(mix_def.items()))

    def form_valid(self, form):
        sender = form.cleaned_data['email']
        my_email = "egorhramkov2002@gmail.com"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        with open("configuration.json") as f:
            password = json.load(f)['password_mail']

        try:
            server.login(my_email, password)
            msg=MIMEText(form.cleaned_data['content'])
            msg['Subject'] = 'От сайта на Django'
            server.sendmail(sender, my_email, msg.as_string())
        except Exception as e:
            print("Ошибка" + str(e))
        return super().form_valid(form)

class NewsSubs(LoginRequiredMixin, DataMixin, ListView):
    model = UserFollowing
    template_name = 'news/newsBySubs.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mix_def = self.get_user_context(title='Новости по подпискам')
        return dict(list(context.items()) + list(mix_def.items()))

    def get_queryset(self):
        uf_list = UserFollowing.objects.filter(following_user=self.request.user.id).select_related('user')
        news_list = []
        for uf in uf_list:
            news_list = list(chain(news_list, News.objects.filter(author=uf.user).select_related('cat', 'author', 'author__profile')))
        return sorted(news_list, key=lambda inst: inst.time_created)[::-1]

@cache_page(60)
@login_required
def searchUserBy(request):
    form = SearchNews()
    if request.method == 'POST':
        form = SearchNews(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("searchBy")
            request.session['search'] = data
        else:
            data=""
        u = User.objects.filter(username__iregex=data).all().select_related('profile')
    else:
        if 'search' in request.session:
            u = User.objects.filter(username__iregex=request.session['search']).all()

    paginator = Paginator(u, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'users': page_obj,
        'form': form,
        'title': 'Список пользователей',
    }
    return render(request, 'news/allUsers.html', context=context)
