from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kitherder.views.home', name='home'),
    # url(r'^kitherder/', include('kitherder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'^admin/', include(admin.site.urls)),
	(r'^$', include('entrance.urls')),
	(r'^entrance/', include('entrance.urls')),
	(r'^userprofile/', include('userprofile.urls')),
	(r'^matchmaker/', include('matchmaker.urls')),
	
)
