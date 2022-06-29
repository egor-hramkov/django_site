from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'time_created')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('time_created',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ("name",)}

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'about', 'profile_pic', 'user_id')
    list_display_links = ('id', 'about', 'profile_pic', 'user_id')
    search_fields = ('id',)

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)


