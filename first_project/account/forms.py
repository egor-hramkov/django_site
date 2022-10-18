from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from account.models import Profile
from news.models import *

class EditProfileForm(forms.ModelForm):
    about = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': "О себе"}), required=False)
    profile_pic = forms.ImageField(label="Загрузите ваш аватар: ", required=False)

    class Meta:
       model = Profile
       fields = ['about', 'profile_pic']
