from gameshop.models import Game, Profile, Developer, Genre, Game_state
from django.shortcuts import get_object_or_404

def getUserContext(user):
    if not user or user.is_anonymous:
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

def getGenre(genre):
    return get_object_or_404(Genre, name=genre)

def getHighScores(game):
    states = Game_state.objects.filter(game=game).order_by("submitted_score")[:5]
    highscores = map(lambda x: (x.profile.user.username, x.submitted_score), states)
    return highscores

def modifyGameIfAuthorized(game_id, form, developer):
    game = get_object_or_404(Game, pk=game_id)

    if not developer.owns(game):
        return Unauthorized()

    game.name = form.cleaned_data.get('name')
    game.description = form.cleaned_data.get('description')
    game.genre = getGenre(form.cleaned_data.get('genre'))
    game.price = form.cleaned_data.get("price")
    game.url = form.cleaned_data.get("url")
    game.save()


def createGame(form, developer):
    game = Game.objects.create(
                    name=form.cleaned_data.get('name'), 
                    description=form.cleaned_data.get('description'),
                    genre=form.cleaned_data.get('genre'), 
                    price=form.cleaned_data.get('price'),
                    url=form.cleaned_data.get('url'), 
                    owner=developer)
    game.save()
