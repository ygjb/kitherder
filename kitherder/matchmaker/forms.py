from django.forms import ModelForm, Textarea, HiddenInput
from django import forms
from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee, Milestone

class ProjectForm(ModelForm):
    class Meta:
        model = Project
		
class MilestoneForm(ModelForm):
	class Meta:
		model = Milestone
		

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
		
class MenteeEditProjectForm(ProjectForm):
	class Meta(ProjectForm.Meta):
		exclude = ('MentorID', 'MenteeID', 'DivisionID', 'TermsAgree', 'Approved', 'ApprovedBy', 'ProjectStatusID')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

class MentorEditProjectForm(ProjectForm):
	class Meta(ProjectForm.Meta):
		exclude = ('MentorID', 'MenteeID', 'DivisionID', 'TermsAgree', 'Approved', 'ApprovedBy')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }	

class CoordinatorEditProjectForm(ProjectForm):
	class Meta(ProjectForm.Meta):
		exclude = ('MentorID', 'MenteeID', 'TermsAgree', 'Approved', 'ApprovedBy')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }	
		
class MentorMenteeMilestoneForm(MilestoneForm):
	class Meta(MilestoneForm.Meta):
		widgets = {
			'ProjectID': HiddenInput,
			'MilestoneComments': Textarea(attrs={'cols': 30, 'rows': 10}),
        }
