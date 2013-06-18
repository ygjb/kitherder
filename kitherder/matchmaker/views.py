# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from matchmaker.models import Project, Division
from django.http import HttpResponse

def myprojects(request):
	myprojectlist = Project.objects.filter(DivisionID__DivisionName="Security")
	#myprojectlist = Project.objects.filter(DivisionID='1')
	return render_to_response('matchmaker/templates/myprojects.html', {'myprojectlist': myprojectlist})
	
def projectdetail(request, projectID):
	theproject = Project.objects.get(pk=projectID)
	return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject})