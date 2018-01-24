from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from gameshop.models import Game
from gameshop.forms import CustomSignUpForm

def about(request):
    return HttpResponse("about page")

def home(request):
    #return render(request, "gameshop/home.html", {}, content_type = 'text/html')
    if request.user != None:
        print(request.user.username + " is logged in")

    template = loader.get_template("gameshop/home.html")
    context = {"user": request.user.username}

    return HttpResponse(template.render(context))

def register(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = CustomSignUpForm()
    return render(request, "gameshop/register.html", {"form": form})

def shop(request):
    template = loader.get_template("gameshop/shop.html")
    gamelist = Game.objects.all()
    context = { "gamelist": gamelist }
    return HttpResponse(template.render(context))

def gamescreen(request):
    return render(request, "gameshop/gamescreen.html", {})

def inventory(request, userView = True):
    template = loader.get_template("gameshop/inventory.html")
    context = {"user": request.user, "userView": userView}
    return HttpResponse(template.render(context))

def dev_inventory(request):
    return inventory(request, False)

#@login_required(login_url='/login/')
def logout_page(request):
    print("Attempt to logout")
    logout(request)
    return render(request, "gameshop/authentication/logout_page.html")

def games(request):
    if request.method == "GET" and request.is_ajax():
        all_games = Game.objects.exclude(bought__user = request.user)
        return render(request, "gameshop/inventory/game_list.html", {"games": all_games, "text": "text"})
    return render(request, "gameshop/games.html")
