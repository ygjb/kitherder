# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.decorators import login_required
	
from django_browserid import get_audience, verify
from django_browserid.forms import BrowserIDForm

from django.contrib.auth.models import User

from matchmaker.models import Mentor, Mentee
from matchmaker.views import findUserRole


class is_lookingForm(forms.Form):
	CHOICES =[('yes', 'yes'), ('no', 'no')]
	is_looking = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

@login_required	
def userprofile(request):
	role = findUserRole(request.user.email)	
	user = User.objects.get(email=request.user.email)
	if role == "mentee":
		mentee = Mentee.objects.get(user_id__email=request.user.email)
		if request.method == 'POST' and "is_looking" in request.POST:
			form = is_lookingForm(request.POST)
			if form.is_valid():
				is_looking = form.cleaned_data['is_looking']
				if is_looking == "yes":
					mentee.is_looking = True;
				else:
					mentee.is_looking = False;
				mentee.save()
				mentee = Mentee.objects.get(user_id__email=request.user.email)
		is_looking = mentee.is_looking
	else:
		is_looking = False

			
	form = is_lookingForm()
	
	return render_to_response('userprofile/templates/profile.html', {'form': form, 'role':role, 'is_looking': is_looking, 'user':user}, context_instance=RequestContext(request))	

