from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from hashlib import md5
import random, json

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    link = models.CharField(max_length=50, default='error')

    def gamesBought(self):
        return Game.objects.filter(bought=self).all()

    def gamesOwned(self):
        return Game.objects.filter(owner=Developer.objects.get(profile=self))

    def hasBought(self, game):
        g = Game.objects.filter(id=game.id).filter(bought=self)
        if g:
            return True
        else:
            return False

    def addGame(self, game):
        self.games_bought.add(game)
        game.addSale()
        self.save()

    def activate(self):
        self.activated = True
        self.save()

    def setLink(self, link):
        self.link = link
        self.save()

    def __str__(self):
        return "\nUsername: " +self.user.username

class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Developer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    studioname = models.CharField(max_length=50)
    
    def owns(self, game):
        return game.owner == self

    def __str__(self):
        return "\nDev profile for user " + self.profile.user.username

class Game(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    sales = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    owner = models.ForeignKey(Developer, on_delete=models.CASCADE)
    #TODO: IMPORTANT REMEMBER TO NOT SET DEFAULT IN PRODUCTION, IT'S ONLY FOR TESTING PURPOSES
    url = models.CharField(max_length=300, default='http://webcourse.cs.hut.fi/example_game.html')
    bought = models.ManyToManyField(Profile, blank=True, through="Game_state")

    def addSale(self):
        self.sales = self.sales + 1
        self.save()

    def addOwner(self, profile):
        state = Game_state(game=self, profile=profile)
        state.save()

    def createChecksum(self):
        secret_key = "b66ccbf9dee582e74d4e80553d361ee2"
        # sys.maxsize?
        pid = random.SystemRandom().randint(0, 100000)
        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, "G621", self.price, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()
        result = """{"%s": "%s", "%s": %s, "%s": "%s"}""" % ("checksum", checksum, "pid", pid, "name", self.name)
        return result

    def __str__(self):
        return "\nName: " + self.name + "\n" \
            + "Description: " + self.description

class Game_state(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    save_score = models.FloatField(default=0)
    save_items = models.TextField(max_length=None, null=True)
    submitted_score = models.FloatField(default=0)

    class Meta:
        unique_together = (("game", "profile"),)

    def save_state(self, score, items):
        self.save_score = score
        self.save_items = items
        self.save()
    
    def submit_score(self, score):
        self.submitted_score = score
        self.save()

    def load_state(self):
        return (self.save_score, self.save_items)

    def __str__(self):
        return "\nGame: " + self.game.name + "\n" \
            + "Profile: " + self.profile.user.username

# Payment class is responsible for knowing which payment with a specific payment id
# (pid) was made and what game is connected to this pid. This data is used when
# showing the completed purchase.
class Payment(models.Model):
    game_id = models.TextField(max_length=None, default="NULL")
    pid = models.TextField(max_length=None, default="NULL")

    def save_payment(self, game_id, pid):
        self.game_id = game_id
        self.pid = pid
        self.save()

    def get_data(self):
        result = """{"game_id": "%s", "pid": %s}""" % (self.game_id, self.pid)
        return result

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
