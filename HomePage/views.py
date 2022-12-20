import datetime
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import CreateUserForm


# Create your views here.
def sign_up(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            messages.error(request, form.errors)

    return render(request, 'HomePage/SignUp.html', context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Неверный логин или пароль!")

    return render(request, 'HomePage/SignIn.html', {})


def home(request):
    return render(request, 'HomePage/HomePage.html', {})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def create_new_meeting(request):
    if request.user.is_authenticated:
        key = (request.user.username + datetime.datetime.now().__str__()).__hash__() + random.randint(0, 500)
        return redirect(f"../../{key}")
    else:
        return redirect('sign-in')


def new_meeting(request, link):
    try:
        if request.user.is_authenticated:
            context = {'link': link,
                       'person_initials': request.user.last_name[0] + request.user.first_name[0],
                       'person_name': request.user.last_name + '_' + request.user.first_name,
                       'person_id': request.user.id
                       }
            return render(request, 'HomePage/Meeting.html', context)
        else:
            return redirect('sign-in')
    except Exception as e:
        print(e)
        return redirect('/')
