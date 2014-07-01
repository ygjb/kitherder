from django.forms import ModelForm, Textarea, HiddenInput, DateInput
from django import forms
from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee, Milestone


class ProjectForm(ModelForm):
	class Meta:
		model = Project

		
class MilestoneForm(ModelForm):
	class Meta:
		model = Milestone
		

class MentorMenteeProjectForm(ProjectForm):
	terms_agree = forms.BooleanField(label='I agree to these terms', required=True)
	class Meta(ProjectForm.Meta):
		exclude = ('mentor_id', 'mentee_id', 'approved', 'approved_by', 'project_status_id')
		widgets = {
			'project_description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

class CoordinatorProjectForm(ProjectForm):
	class Meta(ProjectForm.Meta):
		exclude = ('mentor_id', 'mentee_id', 'approved_by', 'terms_agree')
		widgets = {
			'project_description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
		
class MenteeEditProjectForm(ProjectForm):
	class Meta(ProjectForm.Meta):
		exclude = ('mentor_id', 'mentee_id', 'division_id', 'terms_agree', 'approved', 'approved_by', 'project_status_id')
		widgets = {
			'project_description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }

class MentorEditProjectForm(ProjectForm):
	class Meta(ProjectForm.Meta):
		exclude = ('mentor_id', 'mentee_id', 'division_id', 'terms_agree', 'approved', 'approved_by')
		widgets = {
			'project_description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }	

class CoordinatorEditProjectForm(ProjectForm):
	class Meta(ProjectForm.Meta):
		exclude = ('mentor_id', 'mentee_id', 'terms_agree', 'approved', 'approved_by')
		widgets = {
			'project_description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }	
		
class MentorMenteeMilestoneForm(MilestoneForm):
	class Meta(MilestoneForm.Meta):
		widgets = {
			'project_id': HiddenInput,
			'milestone_comments': Textarea(attrs={'cols': 30, 'rows': 10}),
			'start_date': DateInput(attrs={'class': 'date'}),
			'projected_end_date': DateInput(attrs={'class': 'date'}),
			'completion_date': DateInput(attrs={'class': 'date'}),
        }
