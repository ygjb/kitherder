# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django import forms
from django.db.models import Q
from django.core.context_processors import csrf

from matchmaker.models import Project, Division, Coordinator, User
from matchmaker.forms import ProjectForm


class SearchForm(forms.Form):
    searchterm = forms.CharField(max_length=500)
	

def myprojects(request):
	myprojectslist = Project.objects.filter(DivisionID__DivisionName="Security")
	#myprojectlist = Project.objects.filter(DivisionID='1')
	return render_to_response('matchmaker/templates/myprojects.html', {'myprojectslist': myprojectslist}, context_instance=RequestContext(request))

	
def searchproject(request):
	if request.method == 'POST':
		searched = 1;
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterm = form.cleaned_data['searchterm']
			resultprojectslist = Project.objects.filter(Q(DivisionID__DivisionName__icontains=searchterm) | Q(ProjectName__icontains=searchterm) | Q(ProjectDescription__icontains=searchterm) | Q(SkillsRequired__icontains=searchterm) | Q(ParentProjectID__ProjectName__icontains=searchterm))
			#resultprojectslist = Project.objects.filter(DivisionID__DivisionName="Security")
			#myprojectlist = Project.objects.filter(DivisionID='1')
			return render_to_response('matchmaker/templates/searchproject.html', {'resultprojectslist': resultprojectslist, 'form': form, 'searched': searched}, context_instance=RequestContext(request))
	searched = 0;
	form = SearchForm()
	
	myprojectlist = Project.objects.filter(DivisionID__DivisionName="Security")	
	return render_to_response('matchmaker/templates/searchproject.html', {'myprojectlist': myprojectlist, 'form': form, 'searched': searched}, context_instance=RequestContext(request))

	
def projectdetail(request, projectID):
	theproject = Project.objects.get(pk=projectID)
	mycoordinatorlist = Coordinator.objects.select_related().filter(DivisionID=theproject.DivisionID)
	return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist}, context_instance=RequestContext(request))
	
	
def submitproject(request):
	if request.method == 'POST':
		submitform = ProjectForm(request.POST)
		if form.is_valid():
			model_instance = submitform.save(commit=False)
			model_instance.timestamp = timezone.now()
			model_instance.save()
			return redirect('victory')
	else:
		submitform = ProjectForm()
	return render_to_response('matchmaker/templates/submitproject.html', {'submitform': submitform}, context_instance=RequestContext(request))