from django.contrib import admin

from tumblr.models import *

admin.site.register(TumblrMeta)

admin.site.register(TumblrPost)

admin.site.register(TextPost)
admin.site.register(PhotoPost)
admin.site.register(QuotePost)
admin.site.register(LinkPost)
admin.site.register(ChatPost)
admin.site.register(AudioPost)
admin.site.register(VideoPost)
admin.site.register(AnswerPost)