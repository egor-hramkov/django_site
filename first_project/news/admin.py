from django.contrib import admin
from django.utils.safestring import mark_safe

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
    list_display = ('id', 'about', 'get_html_photo', 'user_id')
    list_display_links = ('id', 'about', 'get_html_photo', 'user_id')
    search_fields = ('id',)

    def get_html_photo(self, object):
        if object.profile_pic:
            return mark_safe(f"<img src='{object.profile_pic.url}', width=50")

    get_html_photo.short_description = 'Фотография пользователя'

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)


