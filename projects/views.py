from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.models import Project
from .forms import CreateProjectForm

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
    if request.method == 'POST':
        #Create a form instance and populate it with data from the request:
        form = CreateProjectForm(request.POST)
        #Check whether it's valid
        if form.is_valid():
            #Get the form data
            name = form.cleaned_data['name']
            manager = request.user
            status = form.cleaned_data['status']
            contributors = form.cleaned_data['contributors']
            description = form.cleaned_data['description']

            #Create the project
            project = Project.objects.create(name = name, manager = manager, status = status, description = description)
            for contributor in contributors:
                project.contributors.add(contributor)

            #Redirect to home
            return redirect('projects:home')
    else:
        form = CreateProjectForm()

    return render(request, "projects/create.html", {'form': form})

def manage_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "managed_projects": request.user.manager.all(),
        "contributed_projects": request.user.contributor.all()
    }
    return render(request, "projects/manage.html", context)

def manage_project_view(request, project_id):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    #Get the project in question
    project = Project.objects.get(pk = project_id)

    #Check whether the user is the contributor, the manager, or viewer
    #Return the appropriate html page
    if project.manager == request.user:
        role = "manager"
    elif project.contributors.filter(id = request.user.id).count() != 0:
        role = "contributor"
    else:
        role = "viewer"
    #Establish the context
    context = {
        "project": project,
        "role": role
    }
    return render(request, "projects/project.html", context)
