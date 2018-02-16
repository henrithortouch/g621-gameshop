from gameshop.models import Game, Profile, Developer, Genre

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