from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm


# Create your views here.
def sign_up(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == 'post':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'HomePage/SignUp.html', context)
