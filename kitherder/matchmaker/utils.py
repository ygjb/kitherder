#helper functions

from matchmaker.models import Project, Division, Coordinator, Mentor, Mentee, Projectstatus, MenteeInterestInProject, Milestone
from matchmaker.forms import ProjectForm, MentorMenteeProjectForm, CoordinatorProjectForm, MenteeEditProjectForm, MentorEditProjectForm, CoordinatorEditProjectForm, MentorMenteeMilestoneForm

import json
import requests


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
			role = "mentor"
		else:
			mentee = Mentee.objects.filter(user_id__email=email)
			if mentee.count() > 0:
				role = "mentee"
	return role


def belongToProject(email, project_id):
	role = findUserRole(email)
	theproject = Project.objects.get(pk=project_id)
	if role == "mentor":
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
	mydivisionlist = Division.objects.select_related().filter(coordinator__user_id__email=email)
	return mydivisionlist

	
def findDivisionsCorrespondingMentor(email):
	mydivisionlist = Division.objects.none()
	
	objs = getMozillianDataByUser(email)
	
	if objs['meta']['total_count'] > 0:
		mydivisionlist = Division.objects.filter(mozillian_group__in = objs['objects'][0]['groups'])
	
	return mydivisionlist


##########################################
## Mozillian API functions
##########################################

	
def getMozillianDataByUser(email):
	url = 'http://192.81.128.7:8000/api/v1/users/?app_name=kitherder&app_key=205dc27dfdb336ec376cb7d70d65f0bd6e10ae28&email=' + email
	r = requests.get(url)

	objs = json.loads(r.text)

	return objs	
	
def getMozillianGroupsbyUser(email):
	groups = getMozillianDataByUser(email)['objects'][0]['groups']

	return groups