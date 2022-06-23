from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('news/', AllNews.as_view(), name='news'),
    path('news/<int:news_id>', newsById.as_view(), name='newsById'),
    path('news/addnews', AddNews.as_view(), name='addNews'),
    path('cats/<slug:cat_slug>', NewsByCat.as_view(), name='category')
]