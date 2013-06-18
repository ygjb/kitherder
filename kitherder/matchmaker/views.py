# Create your views here.

from django.template import Context, loader
from matchmaker.models import Project
from django.http import HttpResponse

def myprojects(request):
	#allprojects = Project.objects.all()
	myprojectlist = Project.objects.get(DivisionID="1")
	t = loader.get_template('matchmaker/templates/myprojects.html')
	c = Context({
		'myprojectlist': myprojectlist,
		})
	return HttpResponse(t)
