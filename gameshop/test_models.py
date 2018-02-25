from django.test import TestCase

from django.contrib.auth.models import User
from gameshop.models import Game, Profile, Genre, Developer

class GameTests(TestCase):

    def setUp(self):
        pass

    def generate_profile(self):
        user = User.objects.create_user("name", "mail", "password")
        return user.profile

    def generate_developer(self):
        p = self.generate_profile()
        dev = Developer.objects.create(profile=p, studioname="test")
        return dev

    def generate_game(self, name, owner):
        genre = Genre.objects.create(name="test")
        game = Game.objects.create(
            name=name,
            description="",
            genre=genre,
            owner=owner)
        return game
