from django.conf.urls.defaults import patterns, include, url


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
    
    url(r'^$', 'kitherder.matchmaker.views.myprojects'),
	url(r'^myprojects', 'kitherder.matchmaker.views.myprojects'),
	# url(r'^matchmaker/submitproject', 'matchmaker.views.submitproject'),
	# url(r'^matchmaker/searchproject', 'matchmaker.views.searchproject'),
    # url(r'^matchmaker/project/(?P<projectID>\d+)/$', 'matchmaker.views.projectdetail'),
    # url(r'^matchmaker/project/(?P<projectID>\d+)/interest/$', 'matchmaker.views.expressinterest'),
    # url(r'^matchmaker/project/(?P<projectID>\d+)/invite/$', 'matchmaker.views.invite'),
	# url(r'^matchmaker/project/(?P<projectID>\d+)/asssign/$', 'matchmaker.views.assign'),
	# url(r'^matchmaker/project/(?P<projectID>\d+)/approve/$', 'matchmaker.views.approve'),
	# url(r'^matchmaker/searchpeople/$', 'matchmaker.views.searchpeople'),
)
