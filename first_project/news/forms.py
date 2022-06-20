from django import forms
from .models import *

class AddNewsForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'addContent'}), label='Текст новости')

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Выберите категорию', label='Категория')