from django.conf.urls import patterns, include, url
from django.contrib import admin

from tumblr.views import single_post, post_archives

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^tumblr/', include('tumblr.urls')),
	url(r'^admin/', include(admin.site.urls)),
	# url(r'^account/', include('registration.backends.default.urls')),
	url(r'^post/(\d+)/$', single_post),
	url(r'^post/(\d+)/([a-z0-9-_]+)$', single_post),
	url(r'^archive$', post_archives)
)