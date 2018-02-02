from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from gameshop.models import Game, Game_state
from gameshop.forms import CustomSignUpForm

import json

def about(request):
    return HttpResponse("about page")

def home(request):
    #return render(request, "gameshop/home.html", {}, content_type = 'text/html')
    if request.user != None:
        print(request.user.username + " is logged in")
    return render(request, "gameshop/home.html", {"user": request.user.username})

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
# Create your views here.

def gamescreen(request, game_id):
    url = Game.objects.get(id = game_id).url
    return render(request, "gameshop/gamescreen.html", {"url": url})

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

#GET request handler
def machine_save_request(request):
        data = dict(request.POST)
        print(data)
        if request.user.is_authenticated :
            u_id = request.user.id
            state = Game_state.objects.get(user__id=u_id)
        return Http404()
