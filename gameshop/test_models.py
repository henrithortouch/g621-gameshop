from django.test import TestCase

from django.contrib.auth.models import User
from gameshop.models import Game, Profile

class GameTests(TestCase):

    def setUp(self):
        pass

    def test_add_game_existing_games_both_exist(self):
        g1 = Game(name = "1", description = "")
        g2 = Game(name = "2", description = "")
        g3 = Game(name = "3", description = "")
        g1.save()
        g2.save()
        g3.save()

        u = self.gen_profile()
        u.addGame(g1)
        u.addGame(g2)

        result = u.games_bought
        self.assertTrue(result.filter(name = "1"))
        self.assertTrue(result.filter(name = "2"))
        self.assertFalse(result.filter(name = "3"))
        self.assertEqual(result.count(), 2)

    def gen_profile(self):
        user = User.objects.create_user("name", "mail", "password")
        return user.profile
