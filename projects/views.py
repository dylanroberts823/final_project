from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.models import Project

# Create your views here.
def home_view(request):
    if not request.user.is_authenticated:
        return render(request, "projects/home.html", {"base": "users/base.html"})
    context = {
        "projects": Project.objects.all(),
        "base":"projects/base.html",
    }
    return render(request, "projects/home.html", context)

def create_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    return render(request, "projects/create.html")

def manage_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    return render(request, "projects/manage.html")
