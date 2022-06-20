from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'category', 'time_created')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('time_created', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ("name",)}

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)


