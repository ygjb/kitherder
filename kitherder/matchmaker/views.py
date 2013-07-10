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

from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee, ProjectStatus, MenteeInterestInProject
from matchmaker.forms import ProjectForm, MentorMenteeProjectForm, CoordinatorProjectForm, MenteeEditProjectForm, MentorEditProjectForm, CoordinatorEditProjectForm


class SearchForm(forms.Form):
    searchterm = forms.CharField(max_length=500)
	
class SearchMenteeForm(forms.Form):
	project = forms.IntegerField(widget=forms.HiddenInput)
	searchterm = forms.CharField(max_length=500)
	
class SearchMentorForm(forms.Form):
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
				return True
		except:
			return False
	elif role == "coordinator":
		# get a list of all the coordinators involved with the project
		coordinatorlist = Coordinator.objects.select_related().filter(DivisionID=theproject.DivisionID)
		currentcoordinator = Coordinator.objects.get(UserID__email=email)
		if currentcoordinator in coordinatorlist:
			return True
	else:
		# assume role is mentee
		try:
			if theproject.MenteeID.UserID.email == email:
				return True
		except:
			return False
	return False
	
def findDivisionsCorrespondingCoordinator(email):
	mydivisionList = Division.objects.select_related().filter(coordinator__UserID__email=email)
	return mydivisionList
	
			

# end helper functions

	
@login_required
def myprojects(request):
	role = findUserRole(request.user.email)
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	
	if role == "vouched mentor" or role == "non-vouched mentor":
		myprojectslist = Project.objects.filter(MentorID__UserID__email=request.user.email)
	elif role == "mentee":
		myprojectslist = Project.objects.filter(MenteeID__UserID__email=request.user.email)
	elif role == "coordinator":
		divisionList = findDivisionsCorrespondingCoordinator(request.user.email)
		myprojectslist = Project.objects.filter(DivisionID__in = divisionList)
		
		if request.method == 'POST' and "approveproject" in request.POST:
			p = Project.objects.get(pk=request.POST['project'])
			c = Coordinator.objects.get(UserID__email=request.user.email)
			p.Approved = True
			p.ApprovedBy = c
			p.save()

	return render_to_response('matchmaker/templates/myprojects.html', {'myprojectslist': myprojectslist, 'role': role}, context_instance=RequestContext(request))	


@login_required	
def searchproject(request):
	role = findUserRole(request.user.email)
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))

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
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	
	isbelong = belongToProject(request.user.email,projectID)

	theproject = Project.objects.get(pk=projectID)
	mycoordinatorlist = Coordinator.objects.select_related().filter(DivisionID=theproject.DivisionID)
	
	# check to see if user is a mentee and is not a member of the project, whether they have expressed interest already in the project
	expressedinterest = 0
	if not isbelong and role == "mentee":
		# if user has clicked on the express interest button
		if request.method == 'POST' and "expressinterest" in request.POST:
			mentee = Mentee.objects.get(UserID__email=request.user.email)
			interest = MenteeInterestInProject(ProjectID=theproject, MenteeID=mentee)
			interest.save()
		expressedinterest = MenteeInterestInProject.objects.filter(MenteeID__UserID__email=request.user.email,ProjectID=projectID).count()
		return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist, 'role': role, 'isbelong': isbelong, 'expressedinterest': expressedinterest}, context_instance=RequestContext(request))
	
	# check to see if user is a mentor and list all mentees who had expressed interest
	if role == "vouched mentor" or  role == "non-vouched mentor" or role =="coordinator":
		# if user has clicked on select mentee to add a mentee from the "expressed interest" list
		# ASSUMPTION: both a vouched and a non vouched mentor can add a mentee who has expressed interest in their project to the project but the triad still has to be approved by coordinator
		# COROLLARY ASSUMPTION: a vouched mentor can add any mentee who is currently marked to be looking for a project (whether they have expressed interest or not)
		if request.method == 'POST' and "selectmentee" in request.POST:
			p = Project.objects.get(pk=request.POST['project'])
			m = Mentee.objects.get(UserID__email=request.POST['selectedmentee'])
			p.MenteeID = m
			p.save()
			theproject = Project.objects.get(pk=projectID)
			
		
		expressedinterestlist = MenteeInterestInProject.objects.filter(ProjectID=projectID)
		return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist, 'role': role, 'isbelong': isbelong, 'expressedinterestlist': expressedinterestlist}, context_instance=RequestContext(request))
	return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist, 'role': role, 'isbelong': isbelong, 'expressedinterest': expressedinterest}, context_instance=RequestContext(request))

@login_required	
def projectedit(request, projectID):
	role = findUserRole(request.user.email)
	redirecturl = '/matchmaker/project/' + str(projectID)
	
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	
	isbelong = belongToProject(request.user.email,projectID)
	if (not isbelong):
		return redirect(redirecturl, context_instance=RequestContext(request))
	
	theproject = Project.objects.get(pk=projectID)
	
	if role == "mentee":
		if request.method == 'POST':
			submitform = MenteeEditProjectForm(request.POST, instance=theproject)
			if submitform.is_valid():
				submitform.save()
				return redirect(redirecturl, context_instance=RequestContext(request))		
		submitform = MenteeEditProjectForm(instance=theproject)

	elif role == "coordinator":
		if request.method == 'POST':
			submitform = CoordinatorEditProjectForm(request.POST, instance=theproject)
			if submitform.is_valid():
				submitform.save()
				return redirect(redirecturl, context_instance=RequestContext(request))
		submitform = CoordinatorEditProjectForm(instance=theproject)

	else:
		if request.method == 'POST':
			submitform = MentorEditProjectForm(request.POST, instance=theproject)
			if submitform.is_valid():
				submitform.save()
				return redirect(redirecturl, context_instance=RequestContext(request))
		submitform = MentorEditProjectForm(instance=theproject)
	
	return render_to_response('matchmaker/templates/projectedit.html', {'theproject': theproject, 'role': role, 'isbelong': isbelong, 'submitform': submitform}, context_instance=RequestContext(request))


@login_required	
def submitproject(request):
	role = findUserRole(request.user.email)	
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	# presenting and inputing forms
	if role == "coordinator":
		if request.method == 'POST':
			submitform = CoordinatorProjectForm(request.POST)
			if submitform.is_valid():
				# assigning all values from form to the object newproject
				newproject = submitform.save(commit=False)
				
				# allow coordinator to approve during submission
				if ("Approved" in request.POST):
					currcoordinator = Coordinator.objects.get(UserID__email=request.user.email)
					newproject.ApprovedBy = currcoordinator
				
				# ASSUMPTION that terms have been agreed on already
				newproject.TermsAgree = True
				
				newproject.save()
				return redirect('/matchmaker/', context_instance=RequestContext(request))		
		else:
			submitform = CoordinatorProjectForm()
			divisionlist = findDivisionsCorrespondingCoordinator(request.user.email)
			parentProjectList = Project.objects.filter(DivisionID__in = divisionlist)
			
			submitform.fields["DivisionID"].queryset = divisionlist
	else:
		if request.method == 'POST':
			submitform = MentorMenteeProjectForm(request.POST)
			if submitform.is_valid():
				# assigning all values from form to the object newproject
				newproject = submitform.save(commit=False)
				
				# setting default status as submitted
				defaultProjectStatus = ProjectStatus.objects.get(Status="submitted")
				newproject.ProjectStatusID = defaultProjectStatus
				
				
				# setting default mentor if logged in user is a mentor		
				if role == "vouched mentor" or role == "non-vouched mentor":
					mentor = Mentor.objects.get(UserID__email=request.user.email)				
					newproject.MentorID = mentor
				elif role == "mentee":
					mentee = Mentee.objects.get(UserID__email=request.user.email)
					newproject.MenteeID = mentee
								
				newproject.save()
				return redirect('/matchmaker/', context_instance=RequestContext(request))
		else:
			submitform = MentorMenteeProjectForm()
	return render_to_response('matchmaker/templates/submitproject.html', {'submitform': submitform, 'role':role,}, context_instance=RequestContext(request))

@login_required
def people(request):
	role = findUserRole(request.user.email)	
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	
	if role != "coordinator":
		return redirect('/matchmaker/myprojects', context_instance=RequestContext(request))
	
	
	if request.method == 'POST':
		mentor = Mentor.objects.get(UserID__email=request.POST["selectedmentor"])
		mentor.IsVouched = True;
		mentor.save()
	
	# get list of projects that have unvouched mentors involved in the coordinator's area
	divisionList = findDivisionsCorrespondingCoordinator(request.user.email)
	projectslist = Project.objects.filter(DivisionID__in = divisionList)
	mentorslist = Mentor.objects.filter(IsVouched=False,pk__in=projectslist)
	
	# get list of all unvouched mentors
	allunvouchedmentors = Mentor.objects.filter(IsVouched=False)
	
		
	return render_to_response('matchmaker/templates/people.html', {'role':role, 'mentorslist':mentorslist, 'allunvouchedmentors':allunvouchedmentors}, context_instance=RequestContext(request))


@login_required	
def searchmentee(request):
	role = findUserRole(request.user.email)	
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))

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
	
	
@login_required	
def searchmentor(request):
	role = findUserRole(request.user.email)	
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))

	project =""
	if request.method == 'POST':
		project = request.POST['project']
		
	if request.method == 'POST' and 'searchterm' in request.POST:
		searched = 1;
		form = SearchMentorForm(request.POST)
		if form.is_valid():
			project = form.cleaned_data['project']
			searchterm = form.cleaned_data['searchterm']
			resultmentorslist = Mentor.objects.filter(UserID__email__icontains=searchterm)
			return render_to_response('matchmaker/templates/mentorfinder.html', {'resultmentorslist': resultmentorslist, 'form': form, 'searched': searched, 'project': project}, context_instance=RequestContext(request))		
			
	if request.method =='POST' and 'selectedmentor' in request.POST:
		p = Project.objects.get(pk=request.POST['project'])
		m = Mentor.objects.get(UserID__email=request.POST['selectedmentor'])
		p.MentorID = m
		p.save()
		return render_to_response('matchmaker/templates/mentorfindersuccess.html', {'mentor': request.POST['selectedmentor'], 'projectname': p.ProjectName}, context_instance=RequestContext(request))		
	
	searched = 0;
	form = SearchMentorForm(initial={'project': project})
	resultmentorslist = Mentor.objects.all()
	return render_to_response('matchmaker/templates/mentorfinder.html', {'resultmentorslist': resultmentorslist, 'form': form, 'searched': searched, 'project': project}, context_instance=RequestContext(request))
	
	
