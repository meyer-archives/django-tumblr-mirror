from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^tumblr/', include('tumblr.urls')),
	url(r'^admin/', include(admin.site.urls)),
	# url(r'^account/', include('registration.backends.default.urls')),
)