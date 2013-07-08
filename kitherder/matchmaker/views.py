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
from matchmaker.forms import ProjectForm, MentorMenteeProjectForm


class SearchForm(forms.Form):
    searchterm = forms.CharField(max_length=500)
	
class SearchMenteeForm(forms.Form):
	project = forms.IntegerField(widget=forms.HiddenInput)
	searchterm = forms.CharField(max_length=500)

# helper functions here
def findUserRole(email):
	# checking to see if the user is a mentor or mentee so we can present the appropriate form
	# always assume most privileged in this case so if user is both mentor and mentee, show for mentor
	role = ""
	coordinator = Coordinator.objects.filter(UserID__email=email)
	if coordinator.count() > 0:
		role = "coordinator"
	else:
		mentor = Mentor.objects.filter(UserID__email=email)
		if mentor.count() > 0:
			if mentor[0].IsVouched == True:
				role = "vouched mentor"
			else:
				role = "non-vouched mentor"
		else:
			mentee = Mentee.objects.filter(UserID__email=email)
			if mentee.count() > 0:
				role = "mentee"
	return role
	
def belongToProject(email, projectid):
	role = findUserRole(email)
	theproject = Project.objects.get(pk=projectid)
	if role == "vouched mentor" or role == "non-vouched mentor":
		try: 
			if theproject.MentorID.UserID.email == email:
				return True;
		except:
			return False;
	elif role == "coordinator":
		# get a list of all the coordinators involved with the project
		# THIS STILL HAS TO BE CHECKED TO SEE IF IT WORKS
		coordinatorlist == Coordinator.objects.select_related().filter(DivisionID=theproject.DivisionID)
		if email in coordinatorlist.UserID.email:
			return True;
	else:
		# assume role is mentee
		try:
			if theproject.MenteeID.UserID.email == email:
				return True;
		except:
			return False;
	return False;
			

# end helper functions

	
@login_required
def myprojects(request):
	role = findUserRole(request.user.email)
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	else:
		if role == "vouched mentor" or role == "non-vouched mentor":
			myprojectslist = Project.objects.filter(MentorID__UserID__email=request.user.email)
		elif role == "mentee":
			myprojectslist = Project.objects.filter(MenteeID__UserID__email=request.user.email)
		return render_to_response('matchmaker/templates/myprojects.html', {'myprojectslist': myprojectslist, 'role': role}, context_instance=RequestContext(request))	

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
	role = findUserRole(request.user.email)
	isbelong = belongToProject(request.user.email,projectID)
	theproject = Project.objects.get(pk=projectID)
	mycoordinatorlist = Coordinator.objects.select_related().filter(DivisionID=theproject.DivisionID)
	return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist, 'role': role, 'isbelong': isbelong}, context_instance=RequestContext(request))
	
@login_required	
def submitproject(request):
	role = findUserRole(request.user.email)	
	# presenting and inputing forms
	if role == "coordinator":
		submitform = ProjectForm(request.POST)
	else:
		if request.method == 'POST':
			submitform = MentorMenteeProjectForm(request.POST)
			if submitform.is_valid():
				# assigning all values from form to the object new project
				newproject = submitform.save(commit=False)
				
				# setting default status as submitted
				defaultProjectStatus = ProjectStatus.objects.get(Status="submitted")
				newproject.ProjectStatusID = defaultProjectStatus
				
				# setting default mentor if logged in user is a mentor		
				if role == "vouched mentor" or role == "non-vouched mentor":
					mentor = Mentor.objects.get(UserID__email=request.user.email)				
					newproject.MentorID = mentor
								
				newproject.save()
				return redirect('/matchmaker/', context_instance=RequestContext(request))
		else:
			submitform = MentorMenteeProjectForm()
	return render_to_response('matchmaker/templates/submitproject.html', {'submitform': submitform}, context_instance=RequestContext(request))
	
@login_required	
def searchmentee(request):
	project =""
	if request.method == 'POST':
		project = request.POST['project']
		
	if request.method == 'POST' and 'searchterm' in request.POST:
		searched = 1;
		form = SearchMenteeForm(request.POST)
		if form.is_valid():
			project = form.cleaned_data['project']
			searchterm = form.cleaned_data['searchterm']
			resultmenteeslist = Mentee.objects.filter(UserID__email__icontains=searchterm, IsLooking=True)
			return render_to_response('matchmaker/templates/menteefinder.html', {'resultmenteeslist': resultmenteeslist, 'form': form, 'searched': searched, 'project': project}, context_instance=RequestContext(request))		
			
	if request.method =='POST' and 'selectedmentee' in request.POST:
		p = Project.objects.get(pk=request.POST['project'])
		m = Mentee.objects.get(UserID__email=request.POST['selectedmentee'])
		p.MenteeID = m
		p.save()
		return render_to_response('matchmaker/templates/menteefindersuccess.html', {'mentee': request.POST['selectedmentee'], 'projectname': p.ProjectName}, context_instance=RequestContext(request))		
	
	searched = 0;
	form = SearchMenteeForm(initial={'project': project})
	resultmenteeslist = Mentee.objects.filter(IsLooking=True)
	return render_to_response('matchmaker/templates/menteefinder.html', {'resultmenteeslist': resultmenteeslist, 'form': form, 'searched': searched, 'project': project}, context_instance=RequestContext(request))