# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserSubscribe'
        db.create_table(u'front_usersubscribe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75, db_index=True)),
        ))
        db.send_create_signal(u'front', ['UserSubscribe'])


    def backwards(self, orm):
        # Deleting model 'UserSubscribe'
        db.delete_table(u'front_usersubscribe')


    models = {
        u'front.autor': {
            'Meta': {'object_name': 'Autor'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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