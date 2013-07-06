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
	return render_to_response('entrance/templates/index.html', context_instance=RequestContext(request))
		
def register(request):
	return render_to_response('entrance/templates/register.html', context_instance=RequestContext(request))	