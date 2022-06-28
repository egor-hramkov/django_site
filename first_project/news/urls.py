from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('news/', AllNews.as_view(), name='news'),
    path('news/<int:news_id>', newsById.as_view(), name='newsById'),
    path('news/addnews', AddNews.as_view(), name='addNews'),
    path('cats/<slug:cat_slug>', NewsByCat.as_view(), name='category'),
    path('news/searchBy', searchNewsBy, name='searchBy'),
    path('register', RegisterUser.as_view(), name='register'),
    path('authorize', Authorize, name='authorize')
]