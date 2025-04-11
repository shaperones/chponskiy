from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from chponskiy.models import LeaderboardRecord

# Create your views here.
def index(request):
    return render(request, 'index.html')


def auth(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
        for field in form:
            match field.name:
                case 'username':
                    field.label = "Username"
                    field.placeholder = "User"
                case 'password':
                    field.label = "Password"
                    field.placeholder = "*****"

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("index")
    else:
        form = UserCreationForm()
        for field in form:
            match field.name:
                case 'username':
                    field.label = "Username"
                    field.placeholder = "user"
                case 'password1':
                    field.label = "Password"
                    field.placeholder = "*****"
                case 'password2':
                    field.label = "Confirm Password"
                    field.placeholder = "*****"

    return render(request, 'register.html', {'form': form})


def leaderboard(request):
    records_top10 = LeaderboardRecord.get_top10()
    return render(request, 'leaderboard.html', {'records': records_top10})


@login_required(login_url="login")
def profile(request):
    return render(request, 'profile.html')
