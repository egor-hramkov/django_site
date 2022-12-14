from django.shortcuts import render
import os.path

from PIL import Image
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, FormView

from first_project.settings import MEDIA_URL, BASE_DIR, MEDIA_ROOT
from .forms import *
from news.models import *
from .utils import DataMixin, menu

import uuid
from itertools import chain

class ShowProfile(LoginRequiredMixin, DataMixin, DetailView):
    model = Profile
    template_name = 'account/profile.html'
    pk_url_kwarg = 'profile_id'
    context_object_name = 'profile'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        us_id = Profile.objects.get(id=self.kwargs['profile_id']).user_id
        context['news'] = News.objects.filter(author_id=us_id)

        f1 = UserFollowing.objects.filter(following_user_id=self.request.user.id, user_id=us_id)
        if f1:
            context['is_flw'] = True
        else:
            context['is_flw'] = False
        mix_def = self.get_user_context(
            title="Профиль пользователя " + User.objects.select_related('profile').get(id=us_id).username)
        return dict(list(context.items()) + list(mix_def.items()))

    def get_queryset(self):
        return Profile.objects.filter(id=self.kwargs['profile_id']).select_related('user')


@login_required
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
    return render(request, 'account/editProfile.html', context=context)

@cache_page(60 * 2)
@login_required
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

@login_required
def following(request):
    if request.GET.get('param') == 'follow':
        UserFollowing.objects.create(following_user_id=request.user.id,
                                     user_id=request.GET.get('usid'))
    elif request.GET.get('param') == 'unfollow':
        if UserFollowing.objects.filter(following_user_id=request.user.id, user_id=request.GET.get('usid')):
            UserFollowing.objects.filter(following_user_id=request.user.id,
                                         user_id=request.GET.get('usid')).delete()
    prof = Profile.objects.get(user_id=request.GET.get('usid'))
    return HttpResponseRedirect(reverse('profile', args=[prof.id]))

class Subs(LoginRequiredMixin, DataMixin, ListView):
    model = UserFollowing
    template_name = 'account/subs.html'
    context_object_name = 'subs'
    paginate_by = 5


    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_usid'] = Profile.objects.select_related('user').get(user_id=self.request.GET.get('usid'))
        mix_def = self.get_user_context(title='Подписки ' + User.objects.select_related('profile')
                                        .get(id=self.request.GET.get('usid'))
                                        .username)
        return dict(list(context.items()) + list(mix_def.items()))

    def get_queryset(self):
        return UserFollowing.objects\
            .filter(following_user_id=self.request.GET.get('usid'))\
            .select_related('following_user', 'user', 'user__profile')

class Followers(LoginRequiredMixin, DataMixin, ListView):
    model = UserFollowing
    template_name = 'account/follower.html'
    context_object_name = 'followers'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_usid'] = Profile.objects.select_related('user').get(user_id=self.request.GET.get('usid'))
        mix_def = self.get_user_context(title='Подписчики пользователя ' + User.objects.select_related('profile')
                                        .get(id=self.request.GET.get('usid'))
                                        .username)
        return dict(list(context.items()) + list(mix_def.items()))

    def get_queryset(self):
        return UserFollowing.objects\
            .filter(user_id=self.request.GET.get('usid'))\
            .select_related('following_user', 'following_user__profile')

