import os.path

from PIL import Image
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from first_project.settings import MEDIA_URL, BASE_DIR, MEDIA_ROOT
from .forms import *
from .models import *
from .utils import DataMixin, menu

import uuid
import PIL

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

class ShowProfile(LoginRequiredMixin, DataMixin, DetailView):
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

    def get_queryset(self):
        return Profile.objects.filter(id=self.kwargs['profile_id']).select_related('user')

def editProfile(request):
    form = EditProfileForm
    if not request.user.is_authenticated:
        raise Http404
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            pu = Profile.objects.get(user_id=request.user.id)
            pu.about = form.cleaned_data['about']
            if form.cleaned_data['profile_pic'] is not None:
                filename = str(pu.profile_pic)
                if filename != "photos/user.png":
                    pathToImg = os.path.join(MEDIA_ROOT, filename)
                    if os.path.isfile(pathToImg):
                        os.remove(pathToImg)
                filename = str(uuid.uuid4())
                file = request.FILES['profile_pic'].read()
                path = os.path.join(MEDIA_ROOT,'photos/', filename + '.png')
                with open(path, 'wb+') as destination:
                    destination.write(file)
                pu.profile_pic = 'photos/' + filename + '.png'
            pu.save()
    else:
        about_user = request.user.profile.about
        form = EditProfileForm(initial={'about': about_user})

    context = {
        'form': form,
        'title': 'Изменить профиль',
        'menu': menu
    }
    return render(request, 'news/editProfile.html', context=context)

def deleteImage(request, img_id):
    prof = Profile.objects.get(id=img_id)
    imgToDel = str(prof.profile_pic)
    if imgToDel != "photos/user.png":
        pathToImg = os.path.join(MEDIA_ROOT, imgToDel)
        if os.path.isfile(pathToImg):
            os.remove(pathToImg)

    prof.profile_pic = "photos/user.png"
    prof.save()
    return HttpResponseRedirect(reverse('profile', args=[prof.id]))

class AllUsers(DataMixin, ListView):
    model = User
    template_name = "news/allUsers.html"
    context_object_name = 'users'
    paginate_by = 3

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchNews()
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
