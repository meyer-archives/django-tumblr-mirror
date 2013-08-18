# TINYAPPS

import os, sys

PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.split(__file__)[0]))
sys.path.insert(0, os.path.join(PROJECT_PATH, "apps"))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Mike Meyer', 'mikemeyer@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'meyerfm',
		'USER': 'webdev',
		'PASSWORD': 'webdev',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}

ALLOWED_HOSTS = []

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
STATIC_ROOT = os.path.join(PROJECT_PATH, "static_cache")

MEDIA_URL = '/media/'
STATIC_URL = '/static_cache/'

STATICFILES_DIRS = (
	os.path.join(PROJECT_PATH, "static"),
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# STATICFILES_STORAGE = ''

AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY_HERE'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_KEY_HERE'
AWS_STORAGE_BUCKET_NAME = 'YOUR_STATIC_BUCKET_HERE'

SIMPLESTATIC_COMPRESSED_DIR = '-'

TUMBLR_REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
TUMBLR_ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'
TUMBLR_AUTHORIZE_URL = 'http://www.tumblr.com/oauth/authorize'

# OAuth keys for mikemeyer.tumblr.com / meyer.fm
TUMBLR_CONSUMER_KEY = 'W7XfPjkuhi1JgnLPt8n9Cz9nDtEc29T5T0lDrC5WmHDXrxb1zF'
TUMBLR_CONSUMER_SECRET = '8wic6HwppRBi9XG8Z8tKRiF9WoHAQniEJ9OC3E85m7TJmQId5n'

# User token/secret for mikemeyer.tumblr.com / meyer.fm
TUMBLR_USER_TOKEN = 'WNsFCMlKqIP1ZTwsKF5AtVp3sCg2G9ANvadUbZmNf7F09wZ7eY'
TUMBLR_USER_SECRET = 'eLxSpzwHebOUSE20MGvsM3OigzKgIAQlC5lW5ZxI2lOagNKAJf'

TUMBLR_CONSUMER_KEY = ''
TUMBLR_CONSUMER_SECRET = ''

# User token/secret for mctestalot.tumblr.com / fakemike.meyer.fm
TUMBLR_USER_TOKEN = ''
TUMBLR_USER_SECRET = ''

TUMBLR_BLOGNAME = 'fakemikemeyer'

SECRET_KEY = '3kr3n1!(=ady#24(rgk@_i12fl*p4oi&&00s_h(klna_b+@*a3'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.static',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',

	'django.core.context_processors.request',

	'django.contrib.auth.context_processors.auth',
	'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (
	# App-specific templates
	# os.path.join(PROJECT_PATH, 'budget', 'templates'),

	# Everything else
	os.path.join(PROJECT_PATH, 'templates'),
)

ACCOUNT_ACTIVATION_DAYS = 7

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.humanize',

	# Third-party
	'simplestatic',
	'south',
	'polymorphic',

	# Third-party, modified
	'django_medusa',

	# My apps
	'utils',
	'tumblr',
)

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

# Static site junk
MEDUSA_RENDERER_CLASS = "django_medusa.renderers.S3StaticSiteRenderer"
MEDUSA_MULTITHREAD = True
AWS_ACCESS_KEY = "AKIAID27ISOEHYY6VDIQ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "medusa-dev"

try:
	from settings_local import *
except ImportError:
	pass