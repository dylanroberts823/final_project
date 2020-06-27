from django.forms import ModelForm
from users.models import Project


class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'status']
