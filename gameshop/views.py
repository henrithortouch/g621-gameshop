from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from gameshop.models import Game, Developer, Profile
from gameshop.forms import CustomSignUpForm
import json
from hashlib import md5

import json

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
    if not request.user.is_anonymous:
        profile = Profile.objects.filter(user = request.user)[0]
    else:
        profile = False
    context = { "gamelist": gamelist, "profile": profile }
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def gamescreen(request, game_id=None):
    try:
        game = Game.objects.get(id = game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound("Specified game was not found")

    url = game.url
    template = loader.get_template("gameshop/gamescreen.html")
    hasGame = request.user.profile.hasBought(game)
    context = { "game": game, "user": request.user, "hasGame": hasGame, "game_url": url}
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def inventory(request, userView = True):
    template = loader.get_template("gameshop/inventory.html")
    prof = Profile.objects.get(user=request.user)
    dev = Developer.objects.filter(profile=prof).first()
        
    context = {"user": request.user, "userView": userView, "developer": dev}
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def dev_inventory(request):
    return inventory(request, False)

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

def buy(request):
    data = dict(request.GET)
    game_id = data["game_id"][0]
    game = Game.objects.filter(id = game_id)[0]
    checksum = game.createChecksum()
    json_data = json.loads(checksum)
    pid = checksum.split(",")[1].split(":")[1].strip()
    request.session[str(pid)] = game_id
    print(game)
    print(json_data)
    return JsonResponse(json_data)

def payment_error(request):
    secret_key = "b66ccbf9dee582e74d4e80553d361ee2"
    return render(request, "gameshop/payment/payment_error.html")

def payment_cancel(request):
    secret_key = "b66ccbf9dee582e74d4e80553d361ee2"
    return render(request, "gameshop/payment/payment_cancel.html")

def payment(request):
    secret_key = "b66ccbf9dee582e74d4e80553d361ee2"
    data = dict(request.GET)
    pid = data["pid"][0]
    ref = data["ref"][0]
    result = data["result"][0]
    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    validate_checksum = data["checksum"][0]
    validation = False
    if validate_checksum == checksum:
        validation = True
    if result == "success" and validation:
        game_id = request.session.get(str(pid))
        #print(game_id)
        game = Game.objects.get(id = game_id)
        profile = Profile.objects.filter(user = request.user)[0]
        if not profile in game.bought.all():
            game.addOwner(profile)
            game.addSale()
        return render(request, "gameshop/payment/payment_success.html")
    elif result == "cancel" and validation:
        game_id = request.session["game_id"] = None
        #print(game_id)
        return render(request, "gameshop/payment/payment_cancel.html")
    else:
        game_id = request.session["game_id"] = None
        #print(game_id)
        return render(request, "gameshop/payment/payment_error.html")

#GET request handler
@login_required(login_url='/login/')
def machine_save_request(request):
    #Not ready yet, do something to this
        data = dict(request.POST)
        print(data)
        if request.user.is_authenticated :
            u_id = request.user.id
            state = Game_state.objects.get(user__id=u_id)
        return Http404()
