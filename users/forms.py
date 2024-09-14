from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username","firstname",'lastname','sex',"type")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ("username","firstname",'lastname','sex',"type")

class CustomUserCreationFormSelf(UserCreationForm):
    adreess =forms.CharField(max_length=10000)
    hospital =forms.IntegerField()
    class Meta:
        model = MyUser
        exclude = ('password','date_joined')
