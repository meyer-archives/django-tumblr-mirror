from django.conf.urls import patterns, include, url

from tumblr.views import *

urlpatterns = patterns('tumblr.views',
	url(r'^$', post_index),
	url(r'^oauth/$', oauth_authenticate),
	url(r'^update/$', update_from_tumblr),
)