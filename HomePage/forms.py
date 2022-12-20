from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Имя (Иван)"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Фамилия (Иванов)"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Логин (Ivanov123)"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Email (Ivanov@mail.ru)"}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Пароль (Ivanov123)"}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Повторите пароль..."}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']