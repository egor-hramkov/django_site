from .models import *

menu = [
    {'title': 'На главную', 'url_name': 'home'},
    {'title': 'Новости', 'url_name': 'news'},
    {'title': 'Опубликовать новость', 'url_name': 'addNews'}
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['menu'] = menu
        context['cats'] = cats

        return context