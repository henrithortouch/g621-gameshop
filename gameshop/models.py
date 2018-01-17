from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Game(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "\nName: " + self.name + "\n" \
            + "Description: " + self.description

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games_bought = models.ManyToManyField(Game)
    games_owned = models.ManyToManyField(Game, through='Ownership')

    def addGame(self, game):
        self.games_bought.add(game)
        self.save()

    def __str__(self):
        return "\nUsername: " +self.user.username + "\n" \
            + "Is dev: %s" % self.is_dev

class Ownership(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sales = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()