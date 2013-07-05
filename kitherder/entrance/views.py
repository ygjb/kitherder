# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import redirect
	
from django_browserid import get_audience, verify
from django_browserid.forms import BrowserIDForm

from django.contrib.auth.models import User

def index(request):
	if request.method == 'POST':
		form = BrowserIDForm(data=request.POST)
		if form.is_valid():
			result = verify(form.cleaned_data['assertion'], get_audience(request))
			if result:
				# check for user account, create account for new users, etc
				userList = User.objects.filter(email=result['email'])
				if userList.objects.count() > 0:
					return render_to_response('entrance/templates/index.html', context_instance=RequestContext(request))
				else:
					return redirect('entrance/register/', context_instance=Requestcontext(request))
			else:
				return redirect('entrance/register/', context_instance=Requestcontext(request))
		else:
			return redirect('entrance/register/', context_instance=Requestcontext(request))
	else:
		return render_to_response('entrance/templates/index.html', context_instance=RequestContext(request))
		
def register(request):
	return render_to_response('entrance/templates/register.html', context_instance=RequestContext(request))	