from django.urls import path

from .views import *

urlpatterns = [
    path('news/', index),
    path('news/<int:news_id>', newsById),
    path('', home, name='home')
]