from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def home_view(request):
    if not request.user.is_authenticated:
        return render(request, "projects/home.html", {"base": "users/base.html"})
    return render(request, "projects/home.html", {"base": "projects/base.html"})

def create_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    return render(request, "projects/create.html")

def manage_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    return render(request, "projects/manage.html")
