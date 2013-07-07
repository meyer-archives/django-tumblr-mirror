from django.conf.urls import patterns, include, url

from tumblr_mirror.views import post_index

urlpatterns = patterns('tumblr_mirror.views',
	url(r'^$', post_index),
)