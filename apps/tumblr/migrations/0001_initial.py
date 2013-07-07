# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TumblrMeta'
        db.create_table(u'tumblr_tumblrmeta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'tumblr', ['TumblrMeta'])

        # Adding model 'TumblrPostTag'
        db.create_table(u'tumblr_tumblrposttag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tag_slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'tumblr', ['TumblrPostTag'])

        # Adding model 'TumblrPost'
        db.create_table(u'tumblr_tumblrpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_tumblr.tumblrpost_set', null=True, to=orm['contenttypes.ContentType'])),
            ('post_id', self.gf('django.db.models.fields.IntegerField')()),
            ('post_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('post_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('post_timestamp', self.gf('django.db.models.fields.IntegerField')()),
            ('post_state', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('post_format', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('post_reblog_key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('note_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'tumblr', ['TumblrPost'])

        # Adding M2M table for field post_tags on 'TumblrPost'
        m2m_table_name = db.shorten_name(u'tumblr_tumblrpost_post_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tumblrpost', models.ForeignKey(orm[u'tumblr.tumblrpost'], null=False)),
            ('tumblrposttag', models.ForeignKey(orm[u'tumblr.tumblrposttag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tumblrpost_id', 'tumblrposttag_id'])

        # Adding model 'TextPost'
        db.create_table(u'tumblr_textpost', (
            (u'tumblrpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tumblr.TumblrPost'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'tumblr', ['TextPost'])

        # Adding model 'TumblrPhoto'
        db.create_table(u'tumblr_tumblrphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'tumblr', ['TumblrPhoto'])

        # Adding model 'PhotoPost'
        db.create_table(u'tumblr_photopost', (
            (u'tumblrpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tumblr.TumblrPost'], unique=True, primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal(u'tumblr', ['PhotoPost'])

        # Adding model 'QuotePost'
        db.create_table(u'tumblr_quotepost', (
            (u'tumblrpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tumblr.TumblrPost'], unique=True, primary_key=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('source_title', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('source', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'tumblr', ['QuotePost'])

        # Adding model 'LinkPost'
        db.create_table(u'tumblr_linkpost', (
            (u'tumblrpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tumblr.TumblrPost'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'tumblr', ['LinkPost'])

        # Adding model 'ChatPost'
        db.create_table(u'tumblr_chatpost', (
            (u'tumblrpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tumblr.TumblrPost'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'tumblr', ['ChatPost'])

        # Adding model 'AudioPost'
        db.create_table(u'tumblr_audiopost', (
            (u'tumblrpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tumblr.TumblrPost'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'tumblr', ['AudioPost'])

        # Adding model 'VideoPost'
        db.create_table(u'tumblr_videopost', (
            (u'tumblrpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tumblr.TumblrPost'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'tumblr', ['VideoPost'])

        # Adding model 'AnswerPost'
        db.create_table(u'tumblr_answerpost', (
            (u'tumblrpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tumblr.TumblrPost'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'tumblr', ['AnswerPost'])


    def backwards(self, orm):
        # Deleting model 'TumblrMeta'
        db.delete_table(u'tumblr_tumblrmeta')

        # Deleting model 'TumblrPostTag'
        db.delete_table(u'tumblr_tumblrposttag')

        # Deleting model 'TumblrPost'
        db.delete_table(u'tumblr_tumblrpost')

        # Removing M2M table for field post_tags on 'TumblrPost'
        db.delete_table(db.shorten_name(u'tumblr_tumblrpost_post_tags'))

        # Deleting model 'TextPost'
        db.delete_table(u'tumblr_textpost')

        # Deleting model 'TumblrPhoto'
        db.delete_table(u'tumblr_tumblrphoto')

        # Deleting model 'PhotoPost'
        db.delete_table(u'tumblr_photopost')

        # Deleting model 'QuotePost'
        db.delete_table(u'tumblr_quotepost')

        # Deleting model 'LinkPost'
        db.delete_table(u'tumblr_linkpost')

        # Deleting model 'ChatPost'
        db.delete_table(u'tumblr_chatpost')

        # Deleting model 'AudioPost'
        db.delete_table(u'tumblr_audiopost')

        # Deleting model 'VideoPost'
        db.delete_table(u'tumblr_videopost')

        # Deleting model 'AnswerPost'
        db.delete_table(u'tumblr_answerpost')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tumblr.answerpost': {
            'Meta': {'object_name': 'AnswerPost', '_ormbases': [u'tumblr.TumblrPost']},
            u'tumblrpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tumblr.TumblrPost']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'tumblr.audiopost': {
            'Meta': {'object_name': 'AudioPost', '_ormbases': [u'tumblr.TumblrPost']},
            u'tumblrpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tumblr.TumblrPost']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'tumblr.chatpost': {
            'Meta': {'object_name': 'ChatPost', '_ormbases': [u'tumblr.TumblrPost']},
            u'tumblrpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tumblr.TumblrPost']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'tumblr.linkpost': {
            'Meta': {'object_name': 'LinkPost', '_ormbases': [u'tumblr.TumblrPost']},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'tumblrpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tumblr.TumblrPost']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'tumblr.photopost': {
            'Meta': {'object_name': 'PhotoPost', '_ormbases': [u'tumblr.TumblrPost']},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            u'tumblrpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tumblr.TumblrPost']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'tumblr.quotepost': {
            'Meta': {'object_name': 'QuotePost', '_ormbases': [u'tumblr.TumblrPost']},
            'source': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'source_title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'tumblrpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tumblr.TumblrPost']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'tumblr.textpost': {
            'Meta': {'object_name': 'TextPost', '_ormbases': [u'tumblr.TumblrPost']},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'tumblrpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tumblr.TumblrPost']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'tumblr.tumblrmeta': {
            'Meta': {'object_name': 'TumblrMeta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'tumblr.tumblrphoto': {
            'Meta': {'object_name': 'TumblrPhoto'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'tumblr.tumblrpost': {
            'Meta': {'object_name': 'TumblrPost'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_tumblr.tumblrpost_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'post_format': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'post_id': ('django.db.models.fields.IntegerField', [], {}),
            'post_reblog_key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post_state': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'post_tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tumblr.TumblrPostTag']", 'symmetrical': 'False'}),
            'post_timestamp': ('django.db.models.fields.IntegerField', [], {}),
            'post_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'post_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'tumblr.tumblrposttag': {
            'Meta': {'object_name': 'TumblrPostTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tag_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'tumblr.videopost': {
            'Meta': {'object_name': 'VideoPost', '_ormbases': [u'tumblr.TumblrPost']},
            u'tumblrpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tumblr.TumblrPost']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['tumblr']