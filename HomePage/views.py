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

        meetingParticipant = MeetingParticipants.objects.get_or_create(person=participant[0], meeting=meeting)
        meetingParticipant[0].save()
        return redirect(f"../../{key}")
    else:
        return redirect('sign-in')


def new_meeting(request, link):
    try:
        meeting = Meeting.objects.get(link=link)
        if request.user.is_authenticated:
            participant = Participant.objects.get_or_create(person=request.user)
            meetingParticipant = MeetingParticipants.objects.get_or_create(person=participant[0], meeting=meeting)

            if meetingParticipant[0].meeting == meeting:
                context = {'link': link, 'persone': participant[0].id}
                return render(request, 'HomePage/Meeting.html', context)

            meeting.members += 1

            participant[0].save()
            meetingParticipant[0].save()
            meeting.save()

            context = {'link': link, 'persone': request.user.id}
            return render(request, 'HomePage/Meeting.html', context)
        else:
            return redirect('sign-in')
    except Exception as e:
        print(e)
        return redirect('/')
