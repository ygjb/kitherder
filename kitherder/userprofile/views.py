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


class IsLookingForm(forms.Form):
	CHOICES =[('yes', 'yes'), ('no', 'no')]
	islooking = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

@login_required	
def userprofile(request):
	role = findUserRole(request.user.email)	
	user = User.objects.get(email=request.user.email)
	if role == "mentee":
		mentee = Mentee.objects.get(UserID__email=request.user.email)
		if request.method == 'POST' and "islooking" in request.POST:
			form = IsLookingForm(request.POST)
			if form.is_valid():
				islooking = form.cleaned_data['islooking']
				if islooking == "yes":
					mentee.IsLooking = True;
				else:
					mentee.IsLooking = False;
				mentee.save()
				mentee = Mentee.objects.get(UserID__email=request.user.email)
		islooking = mentee.IsLooking
	else:
		islooking = False

			
	form = IsLookingForm()
	
	return render_to_response('userprofile/templates/profile.html', {'form': form, 'role':role, 'islooking': islooking, 'user':user}, context_instance=RequestContext(request))	

