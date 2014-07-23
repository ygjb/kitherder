from matchmaker.models import Division, Mentee, Mentor, Coordinator, Projectstatus, Project, MenteeInterestInProject, Milestone
from django.contrib import admin

admin.site.register(Division)
admin.site.register(Projectstatus)
admin.site.register(Coordinator)
admin.site.register(Mentor)
admin.site.register(Mentee)

admin.site.register(Project)
admin.site.register(MenteeInterestInProject)
admin.site.register(Milestone)
