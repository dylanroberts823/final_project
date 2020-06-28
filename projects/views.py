from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.models import Project, Tag
from .forms import CreateProjectForm, SearchForm

# Create your views here.
def home_view(request):
    #Define initial projects to be returned
    projects = Project.objects.all()

    #Modify the projects to be returned if it's a post request
    if request.method == "POST":
        #Create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        #Check whether it's valid
        if form.is_valid():
            #Since it's valid, filter the projects by their tag
            tag = form.cleaned_data['tag']
            tag = Tag.objects.get(tag = tag)
            projects = Project.objects.filter(tags = tag.id)

    #Determine the base
    if not request.user.is_authenticated: base = "users/base.html"
    else: base = "projects/base.html"

    #Render the page with the appropriate context
    context = {
        "projects": projects,
        "base": base,
        "form": SearchForm()
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

            #Redirect to manage
            return redirect('projects:manage')
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
    #Get the project in question
    project = Project.objects.get(pk = project_id)

    #Check whether the user is the contributor, the manager, or viewer
    #Return the appropriate html page
    if project.manager == request.user:
        #Pre-fill the form with all the appropriate fields
        data = {'name': project.name,
                'description': project.description,
                'status': project.status,
                'contributors': project.contributors.all(),
                'tags': project.tags.all()}
        form = CreateProjectForm(initial=data)

        #Create the context
        context = {'form': form,
                   'project': project}
        return render(request, "projects/project_manager.html", context)

    elif project.contributors.filter(id = request.user.id).count() != 0:
        role = "Contributor"
    else:
        role = "Viewer"
    #Establish the context
    context = {
        "project": project,
        "role": role
    }
    return render(request, "projects/project.html", context)

def modify_project_view(request, project_id):
    if request.method == 'POST':
        #Get the current project
        project = Project.objects.get(pk = project_id)

        #Create a form instance and populate it with data from the request:
        form = CreateProjectForm(request.POST)
        #Check whether it's valid
        if form.is_valid():
            #Edit the project with the form data
            project.name = form.cleaned_data['name']
            project.status = form.cleaned_data['status']
            project.description = form.cleaned_data['description']

            #Create a separate loop for contributors and tags
            project.contributors.clear()
            for contributor in form.cleaned_data['contributors']:
                project.contributors.add(contributor)

            project.tags.clear()
            for tag in form.cleaned_data['tags']:
                project.tags.add(tag)

            project.save()

    #Redirect to manage
    return redirect('projects:manage')
