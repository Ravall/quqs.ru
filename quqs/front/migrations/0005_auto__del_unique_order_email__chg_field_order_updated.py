# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Order', fields ['email']
        db.delete_unique(u'front_order', ['email'])


        # Changing field 'Order.updated'
        db.alter_column(u'front_order', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):
        # Adding unique constraint on 'Order', fields ['email']
        db.create_unique(u'front_order', ['email'])


        # Changing field 'Order.updated'
        db.alter_column(u'front_order', 'updated', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'front.autor': {
            'Meta': {'object_name': 'Autor'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'front.order': {
            'Meta': {'object_name': 'Order'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '10'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'front.ordercards': {
            'Meta': {'object_name': 'OrderCards'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['front.Postcard']"}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['front.Order']"})
        },
        u'front.postcard': {
            'Meta': {'object_name': 'Postcard'},
            'art_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['front.Autor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pc_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'front.shortlinkcardsurl': {
            'Meta': {'object_name': 'ShortLinkCardsUrl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_usage': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_part': ('django.db.models.fields.TextField', [], {}),
            'url_short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '33', 'db_index': 'True'})
        },
        u'front.usersubscribe': {
            'Meta': {'object_name': 'UserSubscribe'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['front']