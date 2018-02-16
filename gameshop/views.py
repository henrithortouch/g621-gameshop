from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from gameshop.models import Game, Developer, Profile
from gameshop.forms import CustomSignUpForm, SubmitGameForm
from django import forms
import json
from hashlib import md5

import json

def getUserContext(user):
    if not user:
        return { "profile": None, "developer": None }
        
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    try:
        developer = Developer.objects.get(profile=profile)
    except Developer.DoesNotExist:
        developer = None

    return { "profile": profile, "developer": developer }

def getGame(game_id):
    try:
        return Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return None



def about(request):
    return HttpResponse("about page")

def home(request):
    template = loader.get_template("gameshop/home.html")
    context = getUserContext(request.user)

    return HttpResponse(template.render(context))

def register(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if form.cleaned_data.get("usertype"):
                dev = Developer.objects.create(profile=user.profile, studioname="Unset")
                dev.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomSignUpForm()
    return render(request, "gameshop/register.html", {"form": form})

def shop(request):
    template = loader.get_template("gameshop/shop.html")
    games = Game.objects.all()

    if not request.user.is_anonymous:
        profile = profile = Profile.objects.get(user = request.user)
        gamelist = map(lambda x: (x, profile.hasBought(x)), games)
    else:
        profile = None
        gamelist = map(lambda x: (x, False), games)
        
    context = getUserContext(request.user)
    context["gamelist"] = gamelist
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
def inventory(request):
    template = loader.get_template("gameshop/inventory/inventory.html")
    context = getUserContext(request.user)
    
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def studio(request):
    template = loader.get_template("gameshop/inventory/studio.html")
    context = getUserContext(request.user)

    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def editgame(request, game_id=None):
    if request.method == "POST":
        return Http404()

    template = "gameshop/inventory/editgame.html"
    game = getGame(game_id)
    context = getUserContext(request.user)
    
    if context["developer"]:
        if game:
            if context["developer"].owns(game):
                if request.method == "POST":
                    return Http404()
                else:
                    form = SubmitGameForm()
                    form.fields["name"].initial = game.name
                    form.fields["description"].initial = game.description
                    form.fields["price"].initial = game.price
                    form.fields["url"].initial = game.url
                    context["game"] = game
                    context["form"] = form
                return render(request, template, context)
        else:
            form = SubmitGameForm()
            context["form"] = form
            return render(request, template, context)
    else:
        return Http404()
    


    return Http401("Unauthorized. You do not own this game.")

#@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return render(request, "gameshop/authentication/logout_page.html")

def games(request):
    try:
        profile = Profile.objects.get(user = request.user)
    except Profile.DoesNotExist:
        profile = None

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
    try:
        game = Game.objects.filter(id = game_id)[0]
        checksum = game.createChecksum()
        json_data = json.loads(checksum)
        pid = checksum.split(",")[1].split(":")[1].strip()
        request.session[str(pid)] = game_id
        return JsonResponse(json_data)
    except Game.DoesNotExist:
        return Http404

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
        try:
            game = Game.objects.get(id = game_id)
        except Game.DoesNotExist:
            return Http404
        profile = Profile.objects.filter(user = request.user)[0]
        if not profile.hasBought(game):
            game.addOwner(profile)
            game.addSale()
            #profile.reduceMoney!!!
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
