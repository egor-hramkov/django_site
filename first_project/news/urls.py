from django.urls import path

from .views import *

urlpatterns = [
    path('news/', news, name='news'),
    path('news/<int:news_id>', newsById, name='newsById'),
    path('', home, name='home'),
    path('cats/<slug:cat_slug>', newsByCat, name='category')
]