from django.db import models
from django.contrib.auth.models import User
# Here is the complete model for kitherder including matchmaker and other apps.

class Division(models.Model):
	DivisionName = models.CharField(max_length=50, unique=True)
	
	def __unicode__(self):
		return self.DivisionName
		
	class Meta:
		ordering = ('DivisionName',)
	
	
class Mentee(models.Model):
	UserID = models.ForeignKey(User, unique=True)
	IsLooking = models.BooleanField()
		
	def __unicode__(self):
		return self.UserID.username	
	
class Mentor(models.Model):
	UserID = models.ForeignKey(User, unique=True)
	IsVouched = models.BooleanField()
	
	
	def __unicode__(self):
		return self.UserID.username

class Coordinator(models.Model):
	UserID = models.ForeignKey(User, unique=True)
	DivisionID = models.ManyToManyField(Division)
	IsVouched = models.BooleanField()
	
	def __unicode__(self):
		return self.UserID.username	
	
class ProjectStatus(models.Model):
	Status = models.CharField(max_length=30, unique=True)
	Deprecated = models.BooleanField()
	def __unicode__(self):
		return self.Status
	
class Project(models.Model):
	ProjectName = models.CharField(max_length=70, unique=True)
	ParentProjectID = models.ForeignKey('self', null=True, blank=True)
	DivisionID = models.ForeignKey(Division)
	MentorID = models.ForeignKey(Mentor, null=True, blank=True)
	MenteeID = models.ForeignKey(Mentee, null=True, blank=True)
	Approved = models.BooleanField()
	ApprovedBy = models.ForeignKey(Coordinator, null=True, blank=True)
	ProjectDescription = models.CharField(max_length=300)
	TermsAgree = models.BooleanField()
	ProjectStatusID = models.ForeignKey(ProjectStatus)
	SkillsRequired = models.CharField(max_length=300)
	
	def __unicode__(self):
		return self.ProjectName

class MenteeInterestInProject(models.Model):
	ProjectID = models.ForeignKey(Project)
	MenteeID = models.ForeignKey(Mentee)
			
class Milestone(models.Model):
	ProjectID = models.ForeignKey(Project)
	MilestoneName = models.CharField(max_length=100)
	MilestoneStatus = models.CharField(max_length=80)
	MilestoneComments = models.CharField(max_length=500)
	StartDate = models.DateTimeField()
	ProjectedEndDate = models.DateTimeField()
	CompletionDate = models.DateTimeField()
	
	def __unicode__(self):
		return self.MilestoneName
	
	
