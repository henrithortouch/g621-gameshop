from django.test import TestCase

from django.contrib.auth.models import User
from gameshop.models import Game, Profile, Genre, Developer

class GameTests(TestCase):

    def setUp(self):
        pass

    def test_addGame_(self):
        dev = self.generate_developer()
        g1 = self.generate_game("1", dev)
        g2 = self.generate_game("2", dev)

        dev.profile.addGame(g1)

        result = dev.profile.gamesBought()
        self.assertTrue(result.filter(name = "1"))
        self.assertFalse(result.filter(name = "2"))
        self.assertEqual(result.count(), 1)

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
