from django.urls import path

from .views import *

urlpatterns = [
    path('news/', index, name='news'),
    path('news/<int:news_id>', newsById, name='newsById'),
    path('', home, name='home'),
    path('cats/<int:cat_id>', newsByCat, name='category')
]