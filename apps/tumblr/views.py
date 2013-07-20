from django.shortcuts import render

from tumblr.models import (
	TumblrMeta, TumblrPost, TumblrPostTag,
	TextPost,
	PhotoPost,
	QuotePost,
	LinkPost,
	ChatPost,
	AudioPost,
	VideoPost,
	AnswerPost
)

from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.utils.timezone import utc
from django.template.defaultfilters import slugify

import urlparse
import oauth2 as oauth
import pytumblr
import datetime

def post_index(request):
	entries = TumblrPost.objects.all()
	return render(request, 'tumblr/index.html', { 'entries': entries })

def single_post(request, post_id, slug=False):
	print post_id
	print slug

	post = get_object_or_404(TumblrPost, pk=post_id)

	if post.post_slug:
		if post.post_slug == slug:
			print '%s is a match' % post.post_slug
		else:
			print '%s is not a match' % post.post_slug

	return render(request, 'tumblr/single_post.html', {
		'post': post
	})

def post_archives(request):
	posts = TumblrPost.objects.all()
	return render(request, 'tumblr/archive.html', {
		'posts': posts
	})

def update_from_tumblr(request):

	client = pytumblr.TumblrRestClient(
		settings.TUMBLR_CONSUMER_KEY,
		settings.TUMBLR_CONSUMER_SECRET,
		settings.TUMBLR_USER_TOKEN,
		settings.TUMBLR_USER_SECRET
	)

	posts = client.posts(settings.TUMBLR_BLOGNAME,filter='raw')

	userinfo = client.info()
	bloginfo = client.blog_info(settings.TUMBLR_BLOGNAME)

	try:
		most_recent_post = TumblrPost.objects.latest()
	except TumblrPost.DoesNotExist:
		print 'No most recent post exists. Start from the beginning.'
		most_recent_post = None
		pass


	for p in posts['posts']:

		print
		print '====================='

		post_date = datetime.datetime.strptime(p['date'],'%Y-%m-%d %H:%M:%S %Z')
		post_date = post_date.replace(tzinfo=utc)

		post_data = {
			# 'post_id': p['id'],
			'post_url': p['post_url'],
			'post_shorturl': p['short_url'],
			'post_type': p['type'],
			'post_slug': p['slug'],
			'post_date': post_date,
			'post_timestamp': p['timestamp'],
			'post_state': p['state'],
			'post_format': p['format'],
			'post_reblog_key': p['reblog_key'],
			# 'post_tags': p['tags'],
			'note_count': p['note_count'],
			'api_response': simplejson.dumps(p, indent=4),
		}

		if p['type'] ==   'text':
			PostType = TextPost
			post_data.update({
				'title': p['title'],
				'body': p['body'],
			})

		elif p['type'] == 'photo':
			PostType = PhotoPost
			post_data.update({
				'caption': p['caption'],
				# p['width'],
				# p['height'],
				# p['photos'],
			})

		elif p['type'] == 'quote':
			PostType = QuotePost
			post_data.update({
				'text': p['text'],
				'source': p['source'],
			})
		elif p['type'] == 'link':
			PostType = LinkPost
			post_data.update({
				'title': p['title'],
				'url': p['url'],
				'description': p['description'],
			})
		elif p['type'] == 'chat':
			PostType = ChatPost
			'''
			post_data.update({
				'title': p['title'],
				'body': p['body'],
				'dialogue': p['dialogue'],
			})
			'''
		elif p['type'] == 'audio':
			PostType = AudioPost
			'''
			if 'track_number' not in p:
				p['track_number'] = None

			post_data.update({
				'caption': p['caption'],
				'player': p['player'],
				'plays': p['plays'],
				'album_art': p['album_art'],
				'artist': p['artist'],
				'album': p['album'],
				'track_name': p['track_name'],
				'track_number': p['track_number'],
				'year': p['year'],
			})
			'''
		elif p['type'] == 'video':
			PostType = VideoPost
			'''
			post_data.update({
				'caption': p['caption'],
				'player': p['player'],
			})
			'''
		elif p['type'] == 'answer':
			PostType = AnswerPost
			'''
			post_data.update({
				'asking_name': p['asking_name'],
				'asking_url': p['asking_url'],
				'question': p['question'],
				'answer': p['answer'],
			})
			'''
		else:
			raise TumblrPost.DoesNotExist

		o, post_exists = PostType.objects.get_or_create(post_id=p['id'], defaults=post_data)

		for tag in p['tags']:
			t, tag_exists = TumblrPostTag.objects.get_or_create(tag_slug=slugify(tag))
			t.tag_name = tag
			t.save()
			o.post_tags.add(t)

		print o

		for key,value in post_data.items():
			setattr(o, key, value)

		o.save()

		if p['type'] == 'photo':

			for photo in p['photos']:

				print
				print simplejson.dumps(photo, indent=4),
				print

				# get images for po
				# get image from URL
				# create new photo object
				# set FK to o
				# save

		print '====================='
		print

	return_data = {}

	post_post = {}


	return render(request, 'tumblr/update_list.html', return_data)

def oauth_authenticate(request):
	if settings.TUMBLR_USER_TOKEN:
		raise Http404

	consumer_key = settings.TUMBLR_CONSUMER_KEY
	consumer_secret = settings.TUMBLR_CONSUMER_SECRET

	consumer = oauth.Consumer(consumer_key, consumer_secret)
	client = oauth.Client(consumer)

	if not request.GET.get('oauth_verifier', False):
		resp, content = client.request(settings.TUMBLR_REQUEST_TOKEN_URL, "GET")
		if resp['status'] != '200':
			raise Exception("Invalid response %s." % resp['status'])

		request_token = dict(urlparse.parse_qsl(content))

		request.session['request_token'] = request_token

		tumblr_auth_url = "%s?oauth_token=%s" % (
			settings.TUMBLR_AUTHORIZE_URL,
			request_token['oauth_token'],
		)

		return render(request, 'tumblr/oauth_authenticate.html', {
			'tumblr_auth_url': tumblr_auth_url
		})

		return HttpResponseRedirect(tumblr_auth_url)

	else:

		request_token = request.session['request_token']
		oauth_verifier = request.GET['oauth_verifier']

		token = oauth.Token(request_token['oauth_token'],
			request_token['oauth_token_secret'])
		token.set_verifier(oauth_verifier)
		client = oauth.Client(consumer, token)

		resp, content = client.request(settings.TUMBLR_ACCESS_TOKEN_URL, "POST")
		access_token = dict(urlparse.parse_qsl(content))

		if access_token.get('oauth_token',False):
			print 'Valid Key'
			# Store access token

			oauth_token = access_token.get('oauth_token')
			oauth_token_secret = access_token.get('oauth_token_secret')

			return render(request, 'tumblr/oauth_success.html', {
				'oauth_token': oauth_token,
				'oauth_token_secret': oauth_token_secret
			})

		else:
			print 'Invalid Key'

			return render(request, 'tumblr/oauth_error.html', {
				'access_token': access_token
			})
