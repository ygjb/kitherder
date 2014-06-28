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

from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee, Projectstatus, MenteeInterestInProject, Milestone
from matchmaker.forms import ProjectForm, MentorMenteeProjectForm, CoordinatorProjectForm, MenteeEditProjectForm, MentorEditProjectForm, CoordinatorEditProjectForm, MentorMenteeMilestoneForm


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
	# or if coordinator is also a mentor, assume coordinator
	role = ""
	coordinator = Coordinator.objects.filter(user_id__email=email)
	if coordinator.count() > 0:
		role = "coordinator"
	else:
		mentor = Mentor.objects.filter(user_id__email=email)
		if mentor.count() > 0:
			if mentor[0].is_vouched == True:
				role = "vouched mentor"
			else:
				role = "non-vouched mentor"
		else:
			mentee = Mentee.objects.filter(user_id__email=email)
			if mentee.count() > 0:
				role = "mentee"
	return role
	
def belongToProject(email, project_id):
	role = findUserRole(email)
	theproject = Project.objects.get(pk=project_id)
	if role == "vouched mentor" or role == "non-vouched mentor":
		try: 
			if theproject.mentor_id.user_id.email == email:
				return True
		except:
			return False
	elif role == "coordinator":
		# get a list of all the coordinators involved with the project
		coordinatorlist = Coordinator.objects.select_related().filter(division_id=theproject.division_id)
		currentcoordinator = Coordinator.objects.get(user_id__email=email)
		if currentcoordinator in coordinatorlist:
			return True
	else:
		# assume role is mentee
		try:
			if theproject.mentee_id.user_id.email == email:
				return True
		except:
			return False
	return False
	
def findDivisionsCorrespondingCoordinator(email):
	mydivisionList = Division.objects.select_related().filter(coordinator__user_id__email=email)
	return mydivisionList
	
			

# end helper functions

	
@login_required
def myprojects(request):
	role = findUserRole(request.user.email)
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	
	if role == "vouched mentor" or role == "non-vouched mentor":
		myprojectslist = Project.objects.filter(mentor_id__user_id__email=request.user.email)
	elif role == "mentee":
		myprojectslist = Project.objects.filter(mentee_id__user_id__email=request.user.email)
	elif role == "coordinator":
		divisionList = findDivisionsCorrespondingCoordinator(request.user.email)
		myprojectslist = Project.objects.filter(division_id__in = divisionList)
		
		if request.method == 'POST' and "approveproject" in request.POST:
			p = Project.objects.get(pk=request.POST['project'])
			c = Coordinator.objects.get(user_id__email=request.user.email)
			p.approved= True
			p.approved_by = c
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
			resultprojectslist = Project.objects.filter(Q(division_id__division_name__icontains=searchterm) | Q(project_name__icontains=searchterm) | Q(project_description__icontains=searchterm) | Q(skills_required__icontains=searchterm) | Q(parent_project_id__project_name__icontains=searchterm))
			return render_to_response('matchmaker/templates/searchproject.html', {'resultprojectslist': resultprojectslist, 'form': form, 'searched': searched}, context_instance=RequestContext(request))
	searched = 0;
	form = SearchForm()
	
	return render_to_response('matchmaker/templates/searchproject.html', {'form': form, 'searched': searched}, context_instance=RequestContext(request))


@login_required	
def projectdetail(request, project_id):
	status="nothing";
	role = findUserRole(request.user.email)
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	
	isbelong = belongToProject(request.user.email,project_id)

	theproject = Project.objects.get(pk=project_id)
	mycoordinatorlist = Coordinator.objects.select_related().filter(division_id=theproject.division_id)
	

	if request.method == 'POST' and 'deleteMilestone' in request.POST:
		m = Milestone.objects.get(pk=request.POST['milestone'])
		m.delete()
		status="deletedMilestone"
		
	# assume anyone can see the milestones list
	milestoneslist = Milestone.objects.select_related().filter(project_id=project_id)
	
	# check to see if user is a mentee and is not a member of the project, whether they have expressed interest already in the project
	expressedinterest = 0
	if not isbelong and role == "mentee":
		# if user has clicked on the express interest button
		if request.method == 'POST' and "expressinterest" in request.POST:
			mentee = Mentee.objects.get(user_id__email=request.user.email)
			interest = MenteeInterestInProject(project_id=theproject, mentee_id=mentee)
			interest.save()
		expressedinterest = MenteeInterestInProject.objects.filter(mentee_id__user_id__email=request.user.email,project_id=project_id).count()
		return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist, 'milestoneslist': milestoneslist, 'role': role, 'isbelong': isbelong, 'expressedinterest': expressedinterest, 'status': status}, context_instance=RequestContext(request))
	
	
	
	# check to see if user is a mentor and list all mentees who had expressed interest
	if (isbelong and (role == "vouched mentor" or  role == "non-vouched mentor")) or role =="coordinator":
		# if user has clicked on select mentee to add a mentee from the "expressed interest" list
		# ASSUMPTION: both a vouched and a non vouched mentor can add a mentee who has expressed interest in their project to the project but the triad still has to be approved_by coordinator
		# COROLLARY ASSUMPTION: a vouched mentor can add any mentee who is currently marked to be looking for a project (whether they have expressed interest or not)
		if request.method == 'POST' and "selectmentee" in request.POST:
			p = Project.objects.get(pk=request.POST['project'])
			m = Mentee.objects.get(user_id__email=request.POST['selectedmentee'])
			p.mentee_id = m
			p.save()
			theproject = Project.objects.get(pk=project_id)			
		
		expressedinterestlist = MenteeInterestInProject.objects.filter(project_id=project_id)

		return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist, 'milestoneslist': milestoneslist, 'role': role, 'isbelong': isbelong, 'expressedinterestlist': expressedinterestlist, 'status': status}, context_instance=RequestContext(request))
	return render_to_response('matchmaker/templates/projectdetails.html', {'theproject': theproject, 'mycoordinatorlist': mycoordinatorlist, 'milestoneslist': milestoneslist, 'role': role, 'isbelong': isbelong, 'expressedinterest': expressedinterest, 'status': status}, context_instance=RequestContext(request))

@login_required	
def projectedit(request, project_id):
	role = findUserRole(request.user.email)
	redirecturl = '/matchmaker/project/' + str(project_id)
	
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))
	
	isbelong = belongToProject(request.user.email,project_id)
	if (not isbelong):
		return redirect(redirecturl, context_instance=RequestContext(request))
	
	theproject = Project.objects.get(pk=project_id)
	
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
				if ("approved" in request.POST):
					currcoordinator = Coordinator.objects.get(user_id__email=request.user.email)
					newproject.approved_by = currcoordinator
				
				# ASSUMPTION that terms have been agreed on already
				newproject.terms_agree = True
				
				newproject.save()
				return redirect('/matchmaker/', context_instance=RequestContext(request))		
		else:
			submitform = CoordinatorProjectForm()
			divisionlist = findDivisionsCorrespondingCoordinator(request.user.email)
			parentProjectList = Project.objects.filter(division_id__in = divisionlist)
			
			submitform.fields["division_id"].queryset = divisionlist
	else:
		if request.method == 'POST':
			submitform = MentorMenteeProjectForm(request.POST)
			if submitform.is_valid():
				# assigning all values from form to the object newproject
				newproject = submitform.save(commit=False)
				
				# setting default status as submitted
				defaultProjectstatus = Projectstatus.objects.get(status="submitted")
				newproject.project_status_id = defaultProjectstatus
				
				
				# setting default mentor if logged in user is a mentor		
				if role == "vouched mentor" or role == "non-vouched mentor":
					mentor = Mentor.objects.get(user_id__email=request.user.email)				
					newproject.mentor_id = mentor
				elif role == "mentee":
					mentee = Mentee.objects.get(user_id__email=request.user.email)
					newproject.mentee_id = mentee
								
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
		mentor = Mentor.objects.get(user_id__email=request.POST["selectedmentor"])
		mentor.is_vouched = True;
		mentor.save()
	
	# get list of projects that have unvouched mentors involved in the coordinator's area
	divisionList = findDivisionsCorrespondingCoordinator(request.user.email)
	projectslist = Project.objects.filter(division_id__in = divisionList)
	mentorslist = Mentor.objects.filter(is_vouched=False,pk__in=projectslist)
	
	# get list of all unvouched mentors
	allunvouchedmentors = Mentor.objects.filter(is_vouched=False)
	
		
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
			resultmenteeslist = Mentee.objects.filter(user_id__email__icontains=searchterm, is_looking=True)
			return render_to_response('matchmaker/templates/menteefinder.html', {'resultmenteeslist': resultmenteeslist, 'form': form, 'searched': searched, 'project': project}, context_instance=RequestContext(request))		
			
	if request.method =='POST' and 'selectedmentee' in request.POST:
		p = Project.objects.get(pk=request.POST['project'])
		m = Mentee.objects.get(user_id__email=request.POST['selectedmentee'])
		p.mentee_id = m
		p.save()
		return render_to_response('matchmaker/templates/menteefindersuccess.html', {'mentee': request.POST['selectedmentee'], 'project_name': p.project_name}, context_instance=RequestContext(request))		
	
	searched = 0;
	form = SearchMenteeForm(initial={'project': project})
	resultmenteeslist = Mentee.objects.filter(is_looking=True)
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
			resultmentorslist = Mentor.objects.filter(user_id__email__icontains=searchterm)
			return render_to_response('matchmaker/templates/mentorfinder.html', {'resultmentorslist': resultmentorslist, 'form': form, 'searched': searched, 'project': project}, context_instance=RequestContext(request))		
			
	if request.method =='POST' and 'selectedmentor' in request.POST:
		p = Project.objects.get(pk=request.POST['project'])
		m = Mentor.objects.get(user_id__email=request.POST['selectedmentor'])
		p.mentor_id = m
		p.save()
		return render_to_response('matchmaker/templates/mentorfindersuccess.html', {'mentor': request.POST['selectedmentor'], 'project_name': p.project_name}, context_instance=RequestContext(request))		
	
	searched = 0;
	form = SearchMentorForm(initial={'project': project})
	resultmentorslist = Mentor.objects.all()
	return render_to_response('matchmaker/templates/mentorfinder.html', {'resultmentorslist': resultmentorslist, 'form': form, 'searched': searched, 'project': project}, context_instance=RequestContext(request))
	
@login_required	
def milestoneadd(request):
	role = findUserRole(request.user.email)	
	
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))

	project =""
	if request.method == 'POST':
		project = request.POST['project_id']
	
	form = MentorMenteeMilestoneForm(initial={'project_id': project, 'milestone_status': 'started'})
		
	if request.method =='POST' and 'submit' in request.POST:
		form = MentorMenteeMilestoneForm(request.POST)
		if form.is_valid():
			# assigning all values from form to the object new milestone
			newmilestone = form.save(commit=False)
			
			newmilestone.save()
			return render_to_response('matchmaker/templates/milestoneaddsuccess.html', {}, context_instance=RequestContext(request))		
		
	return render_to_response('matchmaker/templates/milestoneadd.html', {'form': form, 'project': project}, context_instance=RequestContext(request))
	
@login_required	
def milestoneedit(request, milestoneID):
	role = findUserRole(request.user.email)	
	
	if role == "":
		return redirect('/entrance/register/', context_instance=RequestContext(request))

	project =""
	if request.method == 'POST':
		themilestone = Milestone.objects.get(pk=milestoneID)
	
	form = MentorMenteeMilestoneForm(instance=themilestone)
	
	
	if request.method =='POST' and 'submit' in request.POST:
		form = MentorMenteeMilestoneForm(request.POST, instance=themilestone)
		if form.is_valid():
			# assigning all values from form to the object newproject
			newmilestone = form.save()
			
			return render_to_response('matchmaker/templates/milestoneaddsuccess.html', {}, context_instance=RequestContext(request))		
		
	return render_to_response('matchmaker/templates/milestoneedit.html', {'form': form}, context_instance=RequestContext(request))
