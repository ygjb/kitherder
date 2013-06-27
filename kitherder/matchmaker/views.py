# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from matchmaker.models import Project, Division, Coordinator, User
from django.http import HttpResponse
from django.template import RequestContext

def myprojects(request):
	myprojectlist = Project.objects.filter(DivisionID__DivisionName="Security")
	#myprojectlist = Project.objects.filter(DivisionID='1')
	return render_to_response('matchmaker/templates/myprojects.html', {'myprojectlist': myprojectlist}, context_instance=RequestContext(request))
	
def projectdetail(request, projectID):
	theproject = Project.objects.get(pk=projectID)
	mycoordinatorlist = Coordinator.objects.select_related().filter(DivisionID=theproject.DivisionID)
	return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist}, context_instance=RequestContext(request))
	
def submitproject(request):
	return render_to_response('matchmaker/templates/submitproject.html', context_instance=RequestContext(request))