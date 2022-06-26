from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Выберите категорию"

    class Meta:
       model = News
       fields = ['title', 'content', 'cat']
       widgets = {
           'content': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'addContent'})
       }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 150:
            raise ValidationError("Длина заголовка превышает 150 символов")
        return title

class SearchNews(forms.Form):
    searchBy = forms.CharField(max_length=150, label="", help_text="",
                               widget=forms.TextInput(attrs={'placeholder': 'Search'}))