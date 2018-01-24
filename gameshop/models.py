from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(default=0)

    def games(self):
        return Game.objects.filter(bought=self).all()

    def owned(self):
        return Game.objects.filter(owner=Developer.objects.get(profile=self))

    def addGame(self, game):
        self.games_bought.add(game)
        game.addSale()
        self.save()

    def __str__(self):
        return "\nUsername: " +self.user.username

class Developer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    studioname = models.CharField(max_length=50)
    
    def __str__(self):
        return "\nDev profile for user " + self.profile.user.username

class Game(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    sales = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    owner = models.ForeignKey(Developer, on_delete=models.CASCADE)
    bought = models.ManyToManyField(Profile, blank=True)

    def addSale(self):
        self.select_for_update()
        self.sales = self.sales + 1
        self.save()
        transaction.commit()

    def addOwner(self, profile):
        self.bought.add(profile)

    def __str__(self):
        return "\nName: " + self.name + "\n" \
            + "Description: " + self.description
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
