from django.db import models

# Create your models here.

class Project(models.Model):
	ProjectName = models.CharField(max_length=70, unique=True)
	ParentProjectID = models.ForeignKey(Project)
	DivisionID = models.ForeignKey(Division)
	MentorID = models.ForeignKey(Mentor)
	MenteeID = models.ForeignKey(Mentee)
	Approved = models.BooleanField()
	ApprovedBy = models.ForeignKey(Coordinator)
	ProjectDescription = models.CharField(max-lenght=300)
	TermsAgree = models.BooleanField()
	ProjectStatusID = models.ForeignKey(ProjectStatus)
	SkillsRequired = models.charField(max_length=300)
	
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
	
class RELCoordinatorDivision(models.Model):
	CoordinatorID = models.ForeignKey(Coordinator)
	DivisionID = models.ForeignKey(Division)
	
class Division(models.Model):
	DivisionName = models.Charfield(max_length=50, unique=True)
	
class ProjectStatus(models.Model):
	ProjectStatus = models.Charfield(max_length=30, unique=True)
	Deprecated = models.BooleanField()
	
class Milestone(models.Model):
	ProjectID = models.ForeignKey(Project)
	MilestoneName = models.CharField(max_length=100)
	MilestoneStatus = models.CharField(max_length=80)
	MilestoneComments = models.CharField(max_length=500)
	StartDate = models.DateTimeField()
	ProjectedEndDate = models.DateTimeField()
	CompletionDate = models.DateTimeField()
	
	