from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('news/', news, name='news'),
    path('news/<int:news_id>', newsById, name='newsById'),
    path('news/addnews', addNews, name='addNews'),
    path('cats/<slug:cat_slug>', newsByCat, name='category')
]