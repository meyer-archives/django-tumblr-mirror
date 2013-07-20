from django.db import models
from polymorphic import PolymorphicModel

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class TumblrMeta(models.Model):
	key = models.CharField(max_length=100, unique=True)
	value = models.TextField()

	def __unicode__(self):
		return u"%s" % self.key

	class Meta:
		verbose_name = verbose_name_plural = 'Tumblr meta'


class TumblrPostTag(models.Model):
	tag_name = models.CharField(max_length=100)
	tag_slug = models.SlugField(unique=True)

	def __unicode__(self):
		return self.tag_name

class TumblrPost(PolymorphicModel):
	post_id = models.BigIntegerField('post ID', primary_key=True)
	post_url = models.URLField('post URL')
	post_shorturl = models.URLField('post short URL')
	post_type = models.CharField(max_length=20)
	post_slug = models.SlugField(blank=True)
	post_date = models.DateTimeField()
	post_timestamp = models.CharField(max_length=10)
	post_state = models.CharField(max_length=20)
	post_format = models.CharField(max_length=20)
	post_reblog_key = models.CharField(max_length=20)
	post_tags = models.ManyToManyField(TumblrPostTag)
	note_count = models.IntegerField(default=0)

	api_response = models.TextField(blank=True)

	def __unicode__(self):
		return u"%s -- %s" % (self.post_type, self.post_id,)

	def get_absolute_url(self):
		p_url = '/post/%s' % self.post_id

		if self.post_slug:
			return '%s/%s' % (p_url,self.post_slug)

		return p_url

	class Meta:
		get_latest_by = 'post_date'
		verbose_name = 'post'
		verbose_name_plural = 'all posts'

# Post Types

class TextPost(TumblrPost):
	title = models.CharField(blank=True, null=True, max_length=150)
	body = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'Text Post: %s' % self.title

class PhotoPost(TumblrPost):
	caption = models.CharField(blank=True, max_length=150)
	# width
	# height

	def __unicode__(self):
		return u'Photo Post: %s' % self.caption

def tumblr_photo_name(instance, filename):
	return filename
	return '/'.join(['content', instance.user.username, filename])

class TumblrPhoto(models.Model):
	photo = models.ImageField(blank=True,upload_to=tumblr_photo_name)
	photo_url = models.URLField()
	caption = models.CharField(blank=True, max_length=150)
	# alt_sizes[]

	blog_post = models.ForeignKey(PhotoPost, related_name='photos')

	def __unicode__(self):
		return u'Photo: %s' % self.photo.image.url

class QuotePost(TumblrPost):
	source_url = models.URLField(blank=True)
	source_title = models.CharField(blank=True, max_length=150)
	text = models.TextField(blank=True)
	source = models.TextField(blank=True)

	def __unicode__(self):
		return u'Quote Post: %s' % self.text

class LinkPost(TumblrPost):
	title = models.CharField(blank=True, null=True, max_length=150)
	url = models.URLField()
	description = models.TextField(blank=True)

	def __unicode__(self):
		return u'Link Post: %s' % self.url

class ChatPost(TumblrPost):
	def __unicode__(self):
		return u'Chat Post'

class AudioPost(TumblrPost):
	def __unicode__(self):
		return u'Audio Post'

class VideoPost(TumblrPost):
	def __unicode__(self):
		return u'Video Post'

class AnswerPost(TumblrPost):
	def __unicode__(self):
		return u'Answer Post'