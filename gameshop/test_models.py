from django.test import TestCase

from gameshop.models import Game, User

class GameTests(TestCase):

    def setUp(self):
        pass

    def test_add_game_adds_game(self):
        g = Game(name = "töhö", description = "lul")
        u = User()
        g.save()
        u.save()
        u.addGame(g)

        result = u.games_bought
        self.assertEqual(result.values().first()["name"], g.name)
        self.assertEqual(result.count(), 1)

    

    def gen_user():
        return User(user_name="")
