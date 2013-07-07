# Create your views here.

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django import forms
from django.db.models import Q
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect

from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee, ProjectStatus
from matchmaker.forms import ProjectForm, NonVouchedMentorProjectForm, VouchedMentorProjectForm, MenteeProjectForm


class SearchForm(forms.Form):
    searchterm = forms.CharField(max_length=500)
	
class SearchMenteeForm(forms.Form):
    searchterm = forms.CharField(max_length=500)
	
@login_required
def myprojects(request):
	mentorList = Mentor.objects.filter(UserID__email=request.user.email)
	menteeList = Mentee.objects.filter(UserID__email=request.user.email)
	coordinatorList = Coordinator.objects.filter(UserID__email=request.user.email)
	if mentorList.count() == 0 and menteeList.count() == 0 and coordinatorList.count() == 0:
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	else:
		myprojectslist = Project.objects.filter(Q(MentorID__UserID__email=request.user.email)|Q(MenteeID__UserID__email=request.user.email))
		return render_to_response('matchmaker/templates/myprojects.html', {'myprojectslist': myprojectslist}, context_instance=RequestContext(request))	

@login_required	
def searchproject(request):
	if request.method == 'POST':
		searched = 1;
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterm = form.cleaned_data['searchterm']
			resultprojectslist = Project.objects.filter(Q(DivisionID__DivisionName__icontains=searchterm) | Q(ProjectName__icontains=searchterm) | Q(ProjectDescription__icontains=searchterm) | Q(SkillsRequired__icontains=searchterm) | Q(ParentProjectID__ProjectName__icontains=searchterm))
			return render_to_response('matchmaker/templates/searchproject.html', {'resultprojectslist': resultprojectslist, 'form': form, 'searched': searched}, context_instance=RequestContext(request))
	searched = 0;
	form = SearchForm()
	
	return render_to_response('matchmaker/templates/searchproject.html', {'form': form, 'searched': searched}, context_instance=RequestContext(request))

@login_required	
def projectdetail(request, projectID):
	theproject = Project.objects.get(pk=projectID)
	mycoordinatorlist = Coordinator.objects.select_related().filter(DivisionID=theproject.DivisionID)
	return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist}, context_instance=RequestContext(request))
	
@login_required	
def submitproject(request):
	# checking to see if the user is a mentor or mentee so we can present the appropriate form
	# always assume most privileged in this case so if user is both mentor and mentee, show for mentor
	role = ""
	coordinator = Coordinator.objects.filter(UserID__email=request.user.email)
	if coordinator.count() > 0:
		role = "coordinator"
	else:
		mentor = Mentor.objects.filter(UserID__email=request.user.email)
		if mentor.count() > 0:
			if mentor[0].IsVouched == True:
				role = "vouched mentor"
			else:
				role = "non-vouched mentor"
		else:
			role = "mentee"
	# end of determining role
		
	# presenting and inputing forms
	if role == "coordinator":
		submitform = ProjectForm(request.POST)
	elif role == "vouched mentor":
		submitform = VouchedMentorProjectForm(request.POST)
	elif role == "non-vouched mentor":
		if request.method == 'POST':
			defaultProjectStatus = ProjectStatus.objects.get(Status="submitted")
			submitform = NonVouchedMentorProjectForm(request.POST)
			newproject = submitform.save(commit=False)
			newproject.MentorID = mentor[0]
			newproject.ProjectStatusID = defaultProjectStatus
			newproject.save()
			return redirect('/matchmaker/', context_instance=RequestContext(request))
		else:
			submitform = NonVouchedMentorProjectForm()
	else:
		if request.method == 'POST':
			defaultProjectStatus = ProjectStatus.objects.get(Status="submitted")
			submitform = MenteeProjectForm(request.POST)
			newproject = submitform.save(commit=False)
			newproject.MenteeID = Mentee.objects.get(UserID__email=request.user.email)
			newproject.ProjectStatusID = defaultProjectStatus
			newproject.save()
			return redirect('/matchmaker/', context_instance=RequestContext(request))
		else:
			submitform = MenteeProjectForm(request.POST)
		
	return render_to_response('matchmaker/templates/submitproject.html', {'submitform': submitform}, context_instance=RequestContext(request))
	
@login_required	
def searchmentee(request):
	if request.method == 'POST':
		searched = 1;
		form = SearchForm(request.POST)
		if form.is_valid():
			searchterm = form.cleaned_data['searchterm']
			resultmenteeslist = Mentee.objects.filter(UserID__email__icontains=searchterm, IsLooking=True)
			return render_to_response('matchmaker/templates/menteefinder.html', {'resultmenteeslist': resultmenteeslist, 'form': form, 'searched': searched}, context_instance=RequestContext(request))
	searched = 0;
	form = SearchForm()
	resultmenteeslist = Mentee.objects.filter(IsLooking=True)
	return render_to_response('matchmaker/templates/menteefinder.html', {'resultmenteeslist': resultmenteeslist, 'form': form, 'searched': searched}, context_instance=RequestContext(request))