from django.forms import ModelForm
from django.forms import forms
from users.models import Project, Tag

class SearchForm(ModelForm):

    class Meta:
        model = Tag
        fields = ['tag']

class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'contributors', 'tags']
