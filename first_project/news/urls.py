from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('news/', AllNews.as_view(), name='news'),
    path('news/<int:news_id>/', newsById.as_view(), name='newsById'),
    path('news/addnews/', cache_page(60)(AddNews.as_view()), name='addNews'),
    path('news/newsbysubs', NewsSubs.as_view(), name='newsSubs'),
    path('news/searchBy', searchNewsBy, name='searchBy'),
    path('cats/<slug:cat_slug>/', NewsByCat.as_view(), name='category'),
    path('register/', cache_page(60)(RegisterUser.as_view()), name='register'),
    path('login/', cache_page(60)(LoginUser.as_view()), name='login'),
    path('logout/', logout_user, name='logout'),
    path('users/', AllUsers.as_view(), name='allUsers'),
    path('users/searchBy', searchUserBy, name='usersSearch'),
    path('contact/', cache_page(60)(ContactFormView.as_view()), name='contact'),
    path('profile/<int:profile_id>/', ShowProfile.as_view(), name='profile'),
    path('profile/editProfile/', editProfile, name='editProfile'),
    path('profile/deleteimage/<int:img_id>', deleteImage, name='deleteimage'),
    path('profile/following/', following, name='following'),
    path('profile/subscriptions/', Subs.as_view(), name='subs'),
    path('profile/followers/', Followers.as_view(), name='followers'),

]