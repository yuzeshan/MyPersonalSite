# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'manager_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'manager', ['Category'])

        # Adding model 'Blog'
        db.create_table(u'manager_blog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('img', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('content', self.gf('ckeditor.fields.RichTextField')()),
            ('add_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('cate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Category'])),
            ('counts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_show', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'manager', ['Blog'])

        # Adding model 'Blog_tag'
        db.create_table(u'manager_blog_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('add_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'manager', ['Blog_tag'])

        # Adding model 'Tag'
        db.create_table(u'manager_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Blog'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Blog_tag'])),
        ))
        db.send_create_signal(u'manager', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'manager_category')

        # Deleting model 'Blog'
        db.delete_table(u'manager_blog')

        # Deleting model 'Blog_tag'
        db.delete_table(u'manager_blog_tag')

        # Deleting model 'Tag'
        db.delete_table(u'manager_tag')


    models = {
        u'manager.blog': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Blog'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Category']"}),
            'content': ('ckeditor.fields.RichTextField', [], {}),
            'counts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'is_show': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'manager.blog_tag': {
            'Meta': {'ordering': "['id']", 'object_name': 'Blog_tag'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'manager.category': {
            'Meta': {'ordering': "['id']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'manager.tag': {
            'Meta': {'object_name': 'Tag'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Blog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Blog_tag']"})
        }
    }

    complete_apps = ['manager']