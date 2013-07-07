from django.forms import ModelForm, Textarea
from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee

class ProjectForm(ModelForm):
    class Meta:
        model = Project

class NonVouchedMentorProjectForm(ModelForm):
	class Meta:
		model = Project
		exclude = ('MentorID', 'MenteeID', 'Approved', 'ApprovedBy', 'ProjectStatusID')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
	
class VouchedMentorProjectForm(ModelForm):
    class Meta:
		model = Project
		exclude = ('MentorID', 'MenteeID', 'Approved', 'ApprovedBy', 'ProjectStatusID')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class MenteeProjectForm(ModelForm):
    class Meta:
		model = Project
		exclude = ('MentorID', 'MenteeID', 'Approved', 'ApprovedBy', 'ProjectStatusID')
		widgets = {
			'ProjectDescription': Textarea(attrs={'cols': 80, 'rows': 10}),
        }