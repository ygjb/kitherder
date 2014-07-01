from django.db import models
from django.contrib.auth.models import User
# Here is the complete model for kitherder including matchmaker and other apps.

class Division(models.Model):
	division_name = models.CharField(max_length=50, unique=True)
	
	def __unicode__(self):
		return self.division_name
		
	class Meta:
		ordering = ('division_name',)
	
	
class Mentee(models.Model):
	user_id = models.ForeignKey(User, unique=True)
	is_looking = models.BooleanField()
		
	def __unicode__(self):
		return self.user_id.username	
	
class Mentor(models.Model):
	user_id = models.ForeignKey(User, unique=True)
	is_vouched = models.BooleanField()
	
	
	def __unicode__(self):
		return self.user_id.username

class Coordinator(models.Model):
	user_id = models.ForeignKey(User, unique=True)
	division_id = models.ManyToManyField(Division)
	# ASSUMPTION: coordinator comes into the system already vouched. Probably admin will add him/her in
	
	def __unicode__(self):
		return self.user_id.username	
	
class Projectstatus(models.Model):
	status = models.CharField(max_length=30, unique=True)
	deprecated = models.BooleanField()
	def __unicode__(self):
		return self.status

# ASSUMPTION: Project:Mentor:Mentee is a one-to-one-to-one relationship	
class Project(models.Model):
	project_name = models.CharField(max_length=70, unique=True)
	parent_project_id = models.ForeignKey('self', null=True, blank=True, verbose_name="Parent project")
	division_id = models.ForeignKey(Division, verbose_name="Division")
	mentor_id = models.ForeignKey(Mentor, null=True, blank=True)
	mentee_id = models.ForeignKey(Mentee, null=True, blank=True)
	approved= models.BooleanField()
	approved_by = models.ForeignKey(Coordinator, null=True, blank=True)
	project_description = models.CharField(max_length=300)
	terms_agree = models.BooleanField()
	project_status_id = models.ForeignKey(Projectstatus)
	skills_required = models.CharField(max_length=300)
	
	def __unicode__(self):
		return self.project_name

class MenteeInterestInProject(models.Model):
	project_id = models.ForeignKey(Project)
	mentee_id = models.ForeignKey(Mentee)
			
class Milestone(models.Model):
	project_id = models.ForeignKey(Project)
	milestone_name = models.CharField(max_length=100)
	milestone_status = models.CharField(max_length=80)
	milestone_comments = models.CharField(max_length=500)
	start_date = models.DateTimeField()
	projected_end_date = models.DateTimeField()
	completion_date = models.DateTimeField(null=True, blank=True )
	
	def __unicode__(self):
		return self.milestone_name
	
	
