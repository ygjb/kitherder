from django.forms import ModelForm, Textarea
from django import forms
from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee

class ProjectForm(ModelForm):
    class Meta:
        model = Project

class MentorMenteeProjectForm(ModelForm):
	TermsAgree = forms.BooleanField(label='I agree to these terms', required=True)
	class Meta:
		model = Project
		exclude = ('MentorID', 'MenteeID', 'Approved', 'ApprovedBy', 'ProjectStatusID')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }