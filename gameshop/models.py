from django.db import models

# Create your models here.
class Game(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "\nName: " + self.name + "\n" \
            + "Description: " + self.description

class User(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user_name = models.CharField(max_length=20)
    is_dev = models.BooleanField(default=False)
    games_bought = models.ManyToManyField(Game)

    def addGame(self, game):
        self.games_bought.add(game)
        self.save()

    def __str__(self):
        return "\nUsername: " +self.user_name + "\n" \
            + "Is dev: %s" % self.is_dev
