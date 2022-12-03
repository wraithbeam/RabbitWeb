import random

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from .models import Meeting, Participant, MeetingParticipants

import datetime


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
        participant = Participant.objects.get_or_create(person=request.user)

        meeting = Meeting(link=key, members=1, admin=participant[0])
        meeting.save()

        MeetingParticipants(person=participant[0], meeting=meeting).save()
        return redirect(f"../../{key}")
    else:
        return redirect('sing-in')


def new_meeting(request, link):
    if request.user.is_authenticated:
        context = {'link': link, 'persone': request.user.id}
        return render(request, 'HomePage/Meeting.html', context)
    else:
        return redirect('sing-in')
