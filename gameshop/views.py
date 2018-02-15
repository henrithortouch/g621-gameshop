from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from gameshop.models import Game, Developer, Profile, Game_state
from gameshop.forms import CustomSignUpForm
import json
from hashlib import md5


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
    return render(request, "gameshop/authentication/register.html", {"form": form})

def shop(request):
    template = loader.get_template("gameshop/shop.html")
    games = Game.objects.all()

    if not request.user.is_anonymous:
        profile = profile = Profile.objects.get(user = request.user)
        gamelist = map(lambda x: (x, profile.hasBought(x)), games)
    else:
        profile = None
        gamelist = map(lambda x: (x, False), games)
    context = { "gamelist": gamelist, "profile": profile, "user": request.user }
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def gamescreen(request, game_id=None):
    try:
        game = Game.objects.get(id = game_id)
    except Game.DoesNotExist:
        return HttpResponseNotFound("Specified game was not found")
    url = game.url
    hasGame = request.user.profile.hasBought(game)
    context = { "game": game, "user": request.user, "hasGame": hasGame, "game_url": url}
    return render(request, "gameshop/gamescreen.html", context)

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

# Handlers for game Save, Score, Load requests
@login_required(login_url='/login/')
def machine_save(request, game_id=None):
    data = dict(request.POST)
    #TODO: Make items a optional parameter to save
    try:
        try:
            items = data['playerItems[]']
            #Convert items to JSON string
            items_json = json.dumps(items)
        except KeyError:
            #No items given in request so make it none
            items_json = None

        score = data['score'][0]
        game = Game.objects.get(id = game_id)
        profile = Profile.objects.get(user = request.user)
        state = Game_state.objects.get(profile = profile, game = game)
        state.save_state(score = score, items = items_json)
    except KeyError:
        return HttpResponse('No post data', status=400)
    except Game.DoesNotExist:
        return HttpResponse('Game not found',status=500)
    except Profile.DoesNotExist:
        return HttpResponse('User not found',status=500)
    except Game_state.DoesNotExist:
        return HttpResponse('Game state not found',status=500)
    return HttpResponse('OK', status=200)


@login_required(login_url='/login/')
def machine_score(request, game_id=None):
    data = dict(request.POST)
    try:
        score = data['score'][0]
        game = Game.objects.get(id = game_id)
        profile = Profile.objects.get(user = request.user)
        state = Game_state.objects.get(profile = profile, game = game)
        state.submit_score(score = score)
    except KeyError:
        return HttpResponse('No post data', status=400)
    except Game.DoesNotExist:
        return HttpResponse('Game not found',status=500)
    except Profile.DoesNotExist:
        return HttpResponse('User not found',status=500)
    except Game_state.DoesNotExist:
        return HttpResponse('Game state not found',status=500)
    return HttpResponse('OK', status=200)


@login_required(login_url='/login/')
def machine_load(request, game_id=None):
    try:
        #TODO: Make items a optional parameter
        game = Game.objects.get(id = game_id)
        profile = Profile.objects.get(user = request.user)
        state = Game_state.objects.get(profile = profile, game = game)
        data = state.load_state()
        if data[1] == 'NOSAVE':
            print("NOTHING SAVED")
            return HttpResponse("No valid save detected", status=204)
    except KeyError:
        return HttpResponse('No post data', status=400)
    except Game.DoesNotExist:
        return HttpResponse('Game not found',status=500)
    except Profile.DoesNotExist:
        return HttpResponse('User not found',status=500)
    except Game_state.DoesNotExist:
        return HttpResponse('Game state not found',status=500)
    
    #Convert JSON string items to objects
    if data[1] is not None:
        response = {
            'score': data[0],
            'playerItems': json.loads(data[1]),
        }
    else:
        response = {
            'score': data[0],
            'playerItems': ''
        }

    return HttpResponse(json.dumps(response), status=200)