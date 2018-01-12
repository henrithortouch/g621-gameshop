from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

# Täällä on sit täbei
def about(request):
	return HttpResponse("about page")

def home(request):
	#return render(request, "gameshop/home.html", {}, content_type = 'text/html')
	template = loader.get_template("gameshop/home.html")
	context = {}
	output = template.render(context)
	return HttpResponse(output)

def login(request):
	return render(request, "gameshop/login.html", {})
# Create your views here.

def gamescreen(request):
    return render(request, "gameshop/game.html", {})
