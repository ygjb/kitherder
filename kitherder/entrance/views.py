# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
	

def index(request):
	return render_to_response('entrance/templates/index.html', context_instance=RequestContext(request))