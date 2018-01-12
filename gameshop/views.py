from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def about(request):
    return HttpResponse("about page")

def home(request):
<<<<<<< HEAD
    #return render(request, "gameshop/home.html", {}, content_type = 'text/html')
    template = loader.get_template("gameshop/home.html")
    context = {}
    output = template.render(context)
    return HttpResponse(output)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, "gameshop/register.html", {"form": form})
=======
	#return render(request, "gameshop/home.html", {}, content_type = 'text/html')
	template = loader.get_template("gameshop/home.html")
	context = {}
	output = template.render(context)
	return HttpResponse(output)

def login(request):
	return render(request, "gameshop/login.html", {})
>>>>>>> ab028ce879c050120c592c4011d7998ba3b3772e
# Create your views here.

def gamescreen(request):
    return render(request, "gameshop/game.html", {})

def inventory(request):
    return render(request, "gameshop/inventory.html")
