from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kitherder.views.home', name='home'),
    # url(r'^kitherder/', include('kitherder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'matchmaker.views.myprojects'),
	url(r'^myprojects', 'matchmaker.views.myprojects'),
	url(r'^submitproject', 'matchmaker.views.submitproject'),
	url(r'^searchproject', 'matchmaker.views.searchproject'),
	url(r'^project/(?P<projectID>\d+)/$', 'matchmaker.views.projectdetail'),
	url(r'^menteefinder', 'matchmaker.views.searchmentee'),
	url(r'^browserid/', include('django_browserid.urls')),
    # url(r'^matchmaker/project/(?P<projectID>\d+)/interest/$', 'matchmaker.views.expressinterest'),
    # url(r'^matchmaker/project/(?P<projectID>\d+)/invite/$', 'matchmaker.views.invite'),
	# url(r'^matchmaker/project/(?P<projectID>\d+)/asssign/$', 'matchmaker.views.assign'),
	# url(r'^matchmaker/project/(?P<projectID>\d+)/approve/$', 'matchmaker.views.approve'),
	# url(r'^matchmaker/searchpeople/$', 'matchmaker.views.searchpeople'),
)

urlpatterns += staticfiles_urlpatterns()