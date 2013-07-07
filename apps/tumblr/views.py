from django.shortcuts import render
from tumblr_mirror.models import TumblrMeta, TumblrPost

def post_index(request):
	entries = TumblrPost.objects.all()
	return render(request, 'tumblr/index.html', { 'entries': entries })