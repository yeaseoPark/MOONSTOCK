from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

from .models import User

SECTOR_CHOICE = {
        ('manufacturing','Manufacturing'),
        ('wholesale','Wholesale business'),
        ('retail','Retail business'),
        ('restaurant','Restaurant business')
    }

class UserForm(UserCreationForm):

    email = forms.EmailField(label="이메일")
    company_sector = forms.ChoiceField(widget=forms.RadioSelect, choices=SECTOR_CHOICE)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email","company_name","company_phone","company_address","company_sector","representative_name","representative_phone")



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email","company_name","company_phone","company_address","company_sector","representative_name","representative_phone"]
