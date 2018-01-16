from django.test import TestCase

from gameshop.models import Game, User

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

        u = self.gen_user()
        u.addGame(g1)
        u.addGame(g2)

        result = u.games_bought
        self.assertTrue(result.filter(name = "1"))
        self.assertTrue(result.filter(name = "2"))
        self.assertFalse(result.filter(name = "3"))
        self.assertEqual(result.count(), 2)

    def gen_user(self):
        u = User(user_name="")
        u.save()
        return u
