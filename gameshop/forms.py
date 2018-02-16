from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from gameshop.models import Game, Genre

class CustomSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length = 30, required = False, help_text = "Optional.")
    last_name = forms.CharField(max_length = 30, required = False, help_text = "Optional.")
    usertype = forms.BooleanField(help_text="Register as game developer?", required=False)
    email = forms.EmailField(max_length=254, required = True, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'usertype')

class SubmitGameForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=500, required=True)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all())
    price = forms.IntegerField(required=True)
    url = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Game
        fields = ('name', 'description', 'genre', 'price', 'url')
