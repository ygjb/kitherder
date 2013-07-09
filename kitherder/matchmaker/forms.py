from django.forms import ModelForm, Textarea
from django import forms
from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee

class ProjectForm(ModelForm):
    class Meta:
        model = Project

class MentorMenteeProjectForm(ProjectForm):
	TermsAgree = forms.BooleanField(label='I agree to these terms', required=True)
	class Meta(ProjectForm.Meta):
		exclude = ('MentorID', 'MenteeID', 'Approved', 'ApprovedBy', 'ProjectStatusID')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

class CoordinatorProjectForm(ProjectForm):
	class Meta(ProjectForm.Meta):
		exclude = ('MentorID', 'MenteeID', 'ApprovedBy', 'TermsAgree')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }