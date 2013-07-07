from django.db import models
from polymorphic import PolymorphicModel

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

POST_TYPE_CHOICES = (
	('t','text post'),
	('p','photo post'),
	('q','quote post'),
	('l','link post'),
	('c','chat post'),
	('a','audio post'),
	('v','video post'),
	('r','answer post'),
)

POST_STATE_CHOICES = (
	('p','published'),
	('d','draft'),
)

POST_FORMAT_CHOICES = (
	('h','HTML'),
	('m','Markdown'),
)

class TumblrMeta(models.Model):
	key = models.CharField(max_length=100, unique=True)
	value = models.TextField()

	def __unicode__(self):
		return u"%s" % self.key


class TumblrPostTag(models.Model):
	tag_name = models.CharField(max_length=100)
	tag_slug = models.SlugField()

	def __unicode__(self):
		return self.tag_name

class TumblrPost(PolymorphicModel):
	post_id = models.IntegerField()
	post_url = models.URLField()
	post_type = models.CharField(max_length=1,choices=POST_TYPE_CHOICES)
	post_date = models.DateTimeField()
	post_timestamp = models.IntegerField()
	post_state = models.CharField(max_length=1, choices=POST_STATE_CHOICES)
	post_format = models.CharField(max_length=1, choices=POST_FORMAT_CHOICES)
	post_reblog_key = models.CharField(max_length=20)
	post_tags = models.ManyToManyField(TumblrPostTag)
	note_count = models.IntegerField(default=0)

	def __unicode__(self):
		return u"%s -- %s" % (self.post_type, self.post_id,)

# Post Types

class TextPost(TumblrPost):
	title = models.CharField(blank=True, null=True, max_length=150)
	body = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return u'Text Post: %s' % title

def tumblr_photo_name(instance, filename):
	# return instance.
	return '/'.join(['content', instance.user.username, filename])

class TumblrPhoto(models.Model):
	photo = models.ImageField(upload_to=tumblr_photo_name)

	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')

	def __unicode__(self):
		return u'Photo: %s' % photo.image.url

class PhotoPost(TumblrPost):
	caption = models.CharField(blank=True, max_length=150)
	photos = generic.GenericRelation(TumblrPhoto)

	def __unicode__(self):
		return u'Photo Post: %s' % self.caption

class QuotePost(TumblrPost):
	source_url = models.URLField(blank=True)
	source_title = models.CharField(blank=True, max_length=150)
	text = models.TextField(blank=True)
	source = models.TextField(blank=True)

	def __unicode__(self):
		return u'Quote Post: %s' % self.text

class LinkPost(TumblrPost):
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