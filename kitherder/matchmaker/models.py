from django.db import models

# Here is the complete model for kitherder including matchmaker and other apps.

class Division(models.Model):
	DivisionName = models.CharField(max_length=50, unique=True)
	
	def __unicode__(self):
		return self.DivisionName
		
	class Meta:
		ordering = ('DivisionName',)
	
class User(models.Model):
	UserID = models.IntegerField(unique=True)
	Email = models.CharField(max_length=50, unique=True)
	IsVouched = models.BooleanField()
	IsAdmin = models.BooleanField()
	
class Mentee(models.Model):
	UserID = models.ForeignKey(User, unique=True)
	
class Mentor(models.Model):
	UserID = models.ForeignKey(User, unique=True)

class Coordinator(models.Model):
	UserID = models.ForeignKey(User, unique=True)
	DivisionID = models.ManyToManyField(Division)
	
	def __unicode__(self):
		return self.UserID
		
	class Meta:
		ordering = ('UserID',)
	
class ProjectStatus(models.Model):
	ProjectStatus = models.CharField(max_length=30, unique=True)
	Deprecated = models.BooleanField()
	
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

class Milestone(models.Model):
	ProjectID = models.ForeignKey(Project)
	MilestoneName = models.CharField(max_length=100)
	MilestoneStatus = models.CharField(max_length=80)
	MilestoneComments = models.CharField(max_length=500)
	StartDate = models.DateTimeField()
	ProjectedEndDate = models.DateTimeField()
	CompletionDate = models.DateTimeField()
	