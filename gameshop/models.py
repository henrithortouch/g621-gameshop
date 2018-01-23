from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

class Game(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    sales = models.IntegerField(default=0)

    def addSale(self):
        self.select_for_update()
        self.sales = self.sales + 1
        self.save()
        transaction.commit()

    def __str__(self):
        return "\nName: " + self.name + "\n" \
            + "Description: " + self.description

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, through='Ownership')

    def addGame(self, game):
        self.games_bought.add(game)
        game.addSale()
        self.save()

    def __str__(self):
        return "\nUsername: " +self.user.username

class Ownership(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    owned = models.BooleanField(default=False)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()