from django import forms

class CreateForm(forms.Form):
    project_name = forms.CharField(label='Project Name', max_length = 100, help_text='100 characters max', error_messages={'required': 'Please enter your project name'})
    project_desccription = forms.CharField(label='Project Description', widget = forms.Textarea)
    
