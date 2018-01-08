from django.shortcuts import render
from django.http import HttpResponse, Http404

def about(request):
	return HttpResponse("about page")

# Create your views here.
