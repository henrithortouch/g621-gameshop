from django.contrib import admin

from .models import Game, Profile, Ownership

admin.site.register(Game)
admin.site.register(Profile)
admin.site.register(Ownership)