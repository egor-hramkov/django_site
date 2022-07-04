from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('news/', AllNews.as_view(), name='news'),
    path('news/<int:news_id>/', newsById.as_view(), name='newsById'),
    path('news/addnews/', AddNews.as_view(), name='addNews'),
    path('cats/<slug:cat_slug>/', NewsByCat.as_view(), name='category'),
    path('news/searchBy', searchNewsBy, name='searchBy'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/<int:profile_id>/', ShowProfile.as_view(), name='profile'),
    path('profile/editProfile/', editProfile, name='editProfile'),
    path('profile/deleteimage/<int:img_id>', deleteImage, name='deleteimage'),
    path('users/', AllUsers.as_view(), name='allUsers'),
    path('contact/', ContactFormView.as_view(), name='contact')
]