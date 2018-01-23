from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

USER_TYPE_CHOICES = (
    ('gamer', 'Gamer'),
    ('developer', 'Developer'),
    ('both', 'Both'),
)

class CustomSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length = 30, required = False, help_text = "Optional.")
    last_name = forms.CharField(max_length = 30, required = False, help_text = "Optional.")
    #password1 = forms.CharField(widget = forms.PasswordInput, help_text = "<p>Your password must contain at least 8 characters.</p>", label = "Password")
    #password2 = forms.CharField(widget = forms.PasswordInput, help_text = "Repeat password", label = "Repeat password")
    usertype = forms.ChoiceField(required = True, widget = forms.Select, choices = USER_TYPE_CHOICES, help_text = "Select your account type based on your usage.")
    #choice = forms.ChoiceField(choices, required = True)
    email = forms.EmailField(max_length=254, required = True, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'usertype')
