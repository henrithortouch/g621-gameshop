from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from gameshop.models import Game, Developer, Profile
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

@login_required(login_url='/login/')
def gamescreen(request, game_id=None):
    try:
        game = Game.objects.get(id = game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound("Specified game was not found")

    template = loader.get_template("gameshop/gamescreen.html")
    hasGame = request.user.profile.hasBought(game)
    context = { "game": game, "user": request.user, "hasGame": hasGame }
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def user_inventory(request):
    template = loader.get_template("gameshop/inventory/user_inventory.html")
    prof = Profile.objects.get(user=request.user)
    dev = Developer.objects.filter(profile=prof).first()
        
    context = {"user": request.user, "developer": dev}
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def dev_inventory(request):
    template = loader.get_template("gameshop/inventory/dev_inventory.html")
    prof = Profile.objects.get(user=request.user)
    dev = Developer.objects.filter(profile=prof).first()

    context = {"user": request.user, "developer": dev}
    return HttpResponse(template.render(context))

#@login_required(login_url='/login/')
def logout_page(request):
    print("Attempt to logout")
    logout(request)
    return render(request, "gameshop/authentication/logout_page.html")

def games(request):
    profile = Profile.objects.filter(user = request.user)[0]
    if request.method == "GET" and request.is_ajax():
        all_games = Game.objects.exclude(bought__user = request.user)
        return render(request, "gameshop/inventory/game_list.html", {"games": all_games, "text": "text"})
    elif request.method == "ADD_MONEY" and request.is_ajax():
        amount = 20
        profile.addMoney(amount)
        return HttpResponse(amount, content_type="text/plain")
    return render(request, "gameshop/games.html", {"profile": profile})
