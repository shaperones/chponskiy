"""Configures views in the app. See each function docstring for more info on each view."""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from chponskiy.models import LeaderboardRecord

def index(request):
    """Renders index page. Since this page is practically
    static initially, no need for any special parameters"""
    return render(request, 'index.html')


def auth(request):
    """Renders login page and handles login form. Implemented
    mostly with Django's internal auth mechanisms"""
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
    """Renders register page and handles register form. Implemented
    mostly with Django's internal auth mechanisms"""
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
    """Renders leaderboard page. Gets top 10 records for each difficulty to form a table"""
    records_top10 = LeaderboardRecord.get_top10()
    return render(request, 'leaderboard.html', {'records': records_top10})


@login_required(login_url="login")
def profile(request):
    """Renders user profile page"""
    return render(request, 'profile.html')
