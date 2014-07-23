# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django import forms

from django.contrib.auth.models import User

from matchmaker.models import Mentor, Mentee

import json
import requests

class RoleForm(forms.Form):
	CHOICES =[('mentor', 'Mentor'), ('mentee', 'Mentee')]
	role = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
	

def index(request):
	return render_to_response('entrance/templates/index.html', context_instance=RequestContext(request))
		
def register(request):
	form = RoleForm()

	if request.method == 'POST':
		currentUser = User.objects.get(email=request.user.email)
		form = RoleForm(request.POST)
		if form.is_valid():
			role = form.cleaned_data['role']
			if role == "mentor":
			
				## Mentors must be vouched in Mozillian, or else they cannot be a mentor! 
				## Check to see if mentor is a vouched Mozillian
				
				url = 'http://192.81.128.7:8000/api/v1/users/?app_name=kitherder&app_key=205dc27dfdb336ec376cb7d70d65f0bd6e10ae28&email=' + request.user.email
				r = requests.get(url)

				objs = json.loads(r.text)
				
				if objs['meta']['total_count'] > 0 and objs['objects'][0]['is_vouched']:
					newMentor = Mentor(user_id=currentUser)
					newMentor.save()
				else:
					not_vouched = 1
					return render_to_response('entrance/templates/register.html', {'form': form, 'not_vouched':not_vouched}, context_instance=RequestContext(request))
			else:
				newMentee = Mentee(user_id=currentUser,is_looking=True)
				newMentee.save()
			return redirect('/matchmaker/', context_instance=RequestContext(request))
			

	return render_to_response('entrance/templates/register.html', {'form': form}, context_instance=RequestContext(request))	