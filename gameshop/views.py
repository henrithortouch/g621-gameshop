from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

def about(request):
	return HttpResponse("about page")

def home(request):
	template = loader.get_template("gameshop/home.html")
	output = template.render(context)
	return HttpResponse(output)
	
# Create your views here.
