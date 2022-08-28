from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('<int:profile_id>/', ShowProfile.as_view(), name='profile'),
    path('editProfile/', editProfile, name='editProfile'),
    path('deleteimage/<int:img_id>', deleteImage, name='deleteimage'),
    path('following/', following, name='following'),
    path('subscriptions/', Subs.as_view(), name='subs'),
    path('followers/', Followers.as_view(), name='followers'),
]