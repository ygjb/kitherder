from django import forms
from matchmaker.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
	