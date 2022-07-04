from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

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

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "Логин"}))
    email = forms.CharField(label="", widget=forms.EmailInput(attrs={'placeholder': "Email"}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': "Пароль"}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': "Повторите пароль"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "Логин"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': "Пароль"}))


class EditProfileForm(forms.ModelForm):
    about = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': "О себе"}), required=False)
    profile_pic = forms.ImageField(label="Загрузите ваш аватар: ", required=False)

    class Meta:
       model = Profile
       fields = ['about', 'profile_pic']

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()