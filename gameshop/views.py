from django.http import HttpResponse, Http404, HttpResponseNotFound, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.core.mail import send_mail

from gameshop.forms import CustomSignUpForm, SubmitGameForm
from gameshop.models import Game, Developer, Profile, Game_state, Payment, Genre
from gameshop.helpers import getUserContext, getGame, getGenre, \
    getHighScores, modifyGameIfAuthorized, createGame
from gameshop.validation import getPID, getChecksum, getChecksum2, checkValidity
import random,json, sys
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
            new_user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            
            pid = random.SystemRandom().randint(0, 100000)
            checksum = getChecksum2(pid, new_user.id)
            
            profile = Profile.objects.get(user__id = new_user.id)
            profile.setLink(checksum)
            
            send_mail(
                'Activate your account at G621',
                'Click this link to activate your account: <a href="localhost:8000/activate/' + checksum + """/" />""",
                'no-reply@g621.com',
                [str(email)],
                fail_silently=False,
            )

            if form.cleaned_data.get("usertype"):
                dev = Developer.objects.create(profile=user.profile, studioname="Unset")
                dev.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomSignUpForm()
    return render(request, "gameshop/authentication/register.html", {"form": form})

def activate(request, activation_link):
    template = loader.get_template("gameshop/authentication/activate.html")
    context = getUserContext(request.user)
    try: 
        profile = Profile.objects.get(link = activation_link)
        profile.activate()
    except Profile.DoesNotExist:
        profile = None

    context["profile"] = profile
    return HttpResponse(template.render(context))


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

    game = get_object_or_404(Game, id=game_id)
    checksum = game.createChecksum()
    json_data = json.loads(checksum)
    pid = getPID(checksum)
    request.session[str(pid)] = game_id
    payment = Payment(game_id = game_id, pid = pid)
    payment.save()
    return JsonResponse(json_data)


# A view for processing the outcome of the payment process, given that it has passed
# the 'Simple Payments' verification phase. Three different outcomes produce their
# respectable views. 
def payment(request):
    profile = get_object_or_404(Profile, user=request.user)

    result = dict(request.GET)["result"][0]
    validation = checkValidity(dict(request.GET))

    if result == "success" and validation:
        game_id = get_object_or_404(Payment, pid=dict(request.GET)["pid"][0]).game_id
        game = get_object_or_404(Game, id=game_id)

        if not profile.hasBought(game): #At this stage we do not support purchasing multiple copies
            game.addOwner(profile)
            game.addSale()
        return render(request, "gameshop/payment/payment_success.html", {"game": game})
    elif result == "cancel" and validation:
        return render(request, "gameshop/payment/payment_cancel.html")
    else:
        return render(request, "gameshop/payment/payment_error.html")

@login_required(login_url='/login/')
def machine_save(request, game_id=None):
    data = dict(request.POST)
    try:
        items = data['playerItems[]']
        items_json = json.dumps(items)
    except KeyError:
        items_json = None

    try:
        score = data['score'][0]
    except KeyError:
        return HttpResponse('No post data', status=400)

    game =  get_object_or_404(Game, id=game_id)
    profile = get_object_or_404(Profile, user = request.user)
    state = get_object_or_404(Game_state, profile = profile, game = game)

    state.save_state(score = score, items = items_json)

    return HttpResponse('OK', status=200)


@login_required(login_url='/login/')
def machine_score(request, game_id=None):
    data = dict(request.POST)
    try:
        score = data['score'][0]
    except KeyError:
        return HttpResponse('No post data', status=400)

    game =  get_object_or_404(Game, id=game_id)
    profile = get_object_or_404(Profile, user = request.user)
    state = get_object_or_404(Game_state, profile = profile, game = game)
    state.submit_score(score = score)

    return HttpResponse('OK', status=200)


@login_required(login_url='/login/')
def machine_load(request, game_id=None):
    game =  get_object_or_404(Game, id=game_id)
    profile = get_object_or_404(Profile, user = request.user)
    state = get_object_or_404(Game_state, profile = profile, game = game)
    data = state.load_state()
    if data[1] == 'NOSAVE':
        return HttpResponse("No valid save detected", status=204)
    
    if data[1]:
        response = {
            'score': data[0],
            'playerItems': json.loads(data[1]),
        }
    else:
        response = {
            'score': data[0],
            'playerItems': [],
        }

    print(response)
    return HttpResponse(json.dumps(response), status=200)
