from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from gameshop.forms import CustomSignUpForm, SubmitGameForm
from gameshop.models import Game, Developer, Profile, Game_state, Payment, Genre
from gameshop.helpers import getUserContext, getGame, getGenre, getHighScores, modifyGameIfAuthorized, createGame

import json
from hashlib import md5

def about(request):
    return HttpResponse("about page")

def home(request):
    template = loader.get_template("gameshop/home.html")
    context = getUserContext(request.user)

    return HttpResponse(template.render(context))

# View for registering your acocunt. Account details are submitted as a custom
# Django form. See forms.py for further details.
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
    return render(request, "gameshop/authentication/register.html", {"form": form})

def shop(request, genre=None):
    template = loader.get_template("gameshop/shop.html")
    if genre:
        g = get_object_or_404(Genre, name=genre)
        games = Game.objects.filter(genre=g)
    else:
        games = Game.objects.all()

    if request.user.is_anonymous:
        profile = None
        gamelist = map(lambda x: (x, False), games)
    else:
        profile = profile = Profile.objects.get(user = request.user)
        gamelist = map(lambda x: (x, profile.hasBought(x)), games)

    context = getUserContext(request.user)
    context["gamelist"] = gamelist # List[Tuple] (Game, UserHasThatGame)
    context["genres"] = Genre.objects.all()
    
    return HttpResponse(template.render(context))

@login_required(login_url='/login/')
def gamescreen(request, game_id=None):
    game = get_object_or_404(Game, pk=game_id)
    url = game.url

    hasGame = request.user.profile.hasBought(game)

    context = getUserContext(request.user)
    context["game"] = game
    context["hasGame"] = hasGame
    context["game_url"] = url
    context["highscores"] = getHighScores(game)
    return render(request, "gameshop/gamescreen.html", context)

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
    context = getUserContext(request.user)
    if not context['developer']:
        redirect('/login/')

    if request.method == "DELETE":
        game = get_object_or_404(Game, pk=game_id)
        if context["developer"].owns(game):
            game.delete()
            return redirect("/studio/")
        else:
            return Unauthorized()

    elif request.method == "POST":
        form = SubmitGameForm(request.POST)

        if form.is_valid():
            if game_id:
                modifyGameIfAuthorized(game_id, form, context["developer"])
            else:
                createGame(form, context["developer"])

        return redirect('/studio/')

    elif request.method == "GET":
        template = "gameshop/inventory/edit_game.html"
        game = getGame(game_id)
        
        if game: #Form has data if modifying existing game
            if context["developer"].owns(game):
                form = SubmitGameForm()
                form.fields["name"].initial = game.name
                form.fields["description"].initial = game.description
                form.fields["genre"].initial = game.genre
                form.fields["price"].initial = game.price
                form.fields["url"].initial = game.url
                context["game"] = game
                context["form"] = form
                return render(request, template, context)
        else: #If adding new game, blank form
            form = SubmitGameForm()
            context["form"] = form
            return render(request, template, context)
    
    return Http404()

#@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    return render(request, "gameshop/authentication/logout_page.html")

# This view is accessed when the user attempts to buy a game. A ajax call is triggered
# when 'Buy now!' button is pressed. All required parameters for payment processing
# is then passed as a JsonResponse for data to be populated in the payment form.
def buy(request):
    data = dict(request.GET)
    game_id = data["game_id"][0]
    try:
        game = Game.objects.filter(id = game_id)[0]
        checksum = game.createChecksum()
        json_data = json.loads(checksum)
        pid = checksum.split(",")[1].split(":")[1].strip()
        request.session[str(pid)] = game_id
        payment = Payment(game_id = game_id, pid = pid)
        payment.save()
        return JsonResponse(json_data)
    except Game.DoesNotExist:
        return Http404

# A view for processing the outcome of the payment process, given that it has passed
# the 'Simple Payments' verification phase. Three different outcomes produce their
# respectable views. 
def payment(request):
    secret_key = "b66ccbf9dee582e74d4e80553d361ee2"
    data = dict(request.GET)
    pid = data["pid"][0]
    ref = data["ref"][0]
    result = data["result"][0]
    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    validate_checksum = data["checksum"][0] #Checksum received from the request
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
        if not profile.hasBought(game): #At this stage we do not support purchasing multiple copies
            game.addOwner(profile)
            game.addSale()

            payment = Payment.objects.filter(pid = pid)
            game_id = payment[0].game_id
            game = Game.objects.get(id = game_id)
            #profile.reduceMoney!!!
        return render(request, "gameshop/payment/payment_success.html", {"game": game})
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
