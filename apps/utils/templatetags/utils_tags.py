from django.template import Library, Node, Variable, loader, TemplateSyntaxError
from django.template.context import Context
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.utils.safestring import mark_safe
from django.contrib.admin.templatetags.admin_list import result_headers
from string import capitalize
import re
from utils.markdown_processors import WrapImgExtension

register = Library()

from django import template
from django.core import urlresolvers

@register.simple_tag(takes_context=True)
def current(context, url_regex, return_value=' class="current"', **kwargs):
	req = context.get('request')
	if req is None:
		return ''
	if re.search(url_regex, req.path_info):
		return return_value
	return ''

def current_url_equals(context, url_name, **kwargs):
	resolved = False
	try:
		resolved = urlresolvers.resolve(context.get('request').path)
	except:
		pass
	matches = resolved and resolved.url_name == url_name
	if matches and kwargs:
		for key in kwargs:
			kwarg = kwargs.get(key)
			resolved_kwarg = resolved.kwargs.get(key)
			if not resolved_kwarg or kwarg != resolved_kwarg:
				return False
	return matches

@register.filter
def camelcase(value):
	if value.lower() == "iphone":
		return "iPhone"
	if value.lower() == "ipad":
		return "iPad"
	if value.lower() == "ipod":
		return "iPod"
	if value.lower() == "imac":
		return "iMac"
	if value.lower() == "macbook":
		return "MacBook"
	if value.lower() == "macbook pro":
		return "MacBookPro"
	if value.lower() == "macbook air":
		return "MacBookAir"
	return "".join([capitalize(w) for w in re.split(re.compile("[\W_]*"), value)])

@register.filter(is_safe=True)
def markdown(value, arg=''):
	import markdown

	extensions = [e for e in arg.split(",") if e]
	wrap_img_ext = WrapImgExtension()
	# markdown.markdown(raw_text, [wrap_img_ext], safe_mode = 'escape')

	extensions.append(wrap_img_ext)

	if extensions and extensions[0] == "safe":
		extensions = extensions[1:]
		return mark_safe(markdown.markdown(
			force_text(value), extensions, safe_mode=True, enable_attributes=False))
	else:
		return mark_safe(markdown.markdown(
			force_text(value), extensions, safe_mode=False))