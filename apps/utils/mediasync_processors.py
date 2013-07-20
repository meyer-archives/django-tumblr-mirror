try:
	import slimmer
	SLIMMER_INSTALLED = True
except ImportError:
	SLIMMER_INSTALLED = False

# python
import os
import re
import sys
import stat
import shutil
from glob import glob
from collections import defaultdict
from cStringIO import StringIO
from subprocess import Popen, PIPE
import warnings

# django 
from django import template
from django.conf import settings
from django.template import TemplateSyntaxError

def has_optimizer(filetype):
	if filetype == 'css':
		if getattr(settings, 'DJANGO_STATIC_YUI_COMPRESSOR', None):
			return True
		return slimmer is not None
	elif filetype == 'js':
		if getattr(settings, 'DJANGO_STATIC_CLOSURE_COMPILER', None):
			return True
		if getattr(settings, 'DJANGO_STATIC_YUI_COMPRESSOR', None):
			return True

		return slimmer is not None
	else:
		raise ValueError("Invalid type %r" % filetype)

def optimize(content, filetype):
	if filetype == 'css':
		if getattr(settings, 'DJANGO_STATIC_YUI_COMPRESSOR', None):
			return _run_yui_compressor(content, filetype)
		return css_slimmer(content)
	elif filetype == 'js':
		if getattr(settings, 'DJANGO_STATIC_CLOSURE_COMPILER', None):
			return _run_closure_compiler(content)
		if getattr(settings, 'DJANGO_STATIC_YUI_COMPRESSOR', None):
			return _run_yui_compressor(content, filetype)
		return js_slimmer(content)
	else:
		raise ValueError("Invalid type %r" % type_)

def _run_closure_compiler(jscode):
	cmd = "%s" % settings.DJANGO_STATIC_CLOSURE_COMPILER
	proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
	try:
		(stdoutdata, stderrdata) = proc.communicate(jscode)
	except OSError, msg:
		# see comment on OSErrors inside _run_yui_compressor()
		stderrdata = \
		  "OSError: %s. Try again by making a small change and reload" % msg
	if stderrdata:
		return "/* ERRORS WHEN RUNNING CLOSURE COMPILER\n" + stderrdata + '\n*/\n' + jscode 

	return stdoutdata

def _run_yui_compressor(code, filetype):
	cmd = "%s --type=%s" % (settings.DJANGO_STATIC_YUI_COMPRESSOR, filetype)
	proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
	try:
		(stdoutdata, stderrdata) = proc.communicate(code)
	except OSError, msg:
		# Sometimes, for unexplicable reasons, you get a Broken pipe when
		# running the popen instance. It's always non-deterministic problem
		# so it probably has something to do with concurrency or something
		# really low level. 
		stderrdata = \
		  "OSError: %s. Try again by making a small change and reload" % msg

	if stderrdata:
		return "/* ERRORS WHEN RUNNING YUI COMPRESSOR\n" + stderrdata + '\n*/\n' + code

	return stdoutdata

def css_minifier(filedata, content_type, remote_path, is_active):
	if content_type == 'text/css' or remote_path.lower().endswith('.css'):
		return _run_yui_compressor(filedata, 'css')

def js_minifier(filedata, content_type, remote_path, is_active):
	if content_type == 'text/javascript' or remote_path.lower().endswith('.js'):
		return _run_closure_compiler(filedata)