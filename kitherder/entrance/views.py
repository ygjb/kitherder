# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django import forms
	
from django_browserid import get_audience, verify
from django_browserid.forms import BrowserIDForm

from django.contrib.auth.models import User

from matchmaker.models import Mentor, Mentee

class RoleForm(forms.Form):
	CHOICES =[('mentor', 'Mentor'), ('mentee', 'Mentee')]
	role = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

def index(request):
	return render_to_response('entrance/templates/index.html', context_instance=RequestContext(request))
		
def register(request):
	if request.method == 'POST':
		currentUser = User.objects.get(email=request.user.email)
		form = RoleForm(request.POST)
		if form.is_valid():
			role = form.cleaned_data['role']
			if role == "mentor":
				newMentor = Mentor(user_id=currentUser)
				newMentor.save()
			else:
				newMentee = Mentee(user_id=currentUser,is_looking=True)
				newMentee.save()
			return redirect('/matchmaker/', context_instance=RequestContext(request))
			
	form = RoleForm()
	return render_to_response('entrance/templates/register.html', {'form': form}, context_instance=RequestContext(request))	