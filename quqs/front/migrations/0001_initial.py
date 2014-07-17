# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Autor'
        db.create_table(u'front_autor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'front', ['Autor'])

        # Adding model 'Postcard'
        db.create_table(u'front_postcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('art_number', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('autor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['front.Autor'])),
            ('pc_image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'front', ['Postcard'])


    def backwards(self, orm):
        # Deleting model 'Autor'
        db.delete_table(u'front_autor')

        # Deleting model 'Postcard'
        db.delete_table(u'front_postcard')


    models = {
        u'front.autor': {
            'Meta': {'object_name': 'Autor'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'front.postcard': {
            'Meta': {'object_name': 'Postcard'},
            'art_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['front.Autor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pc_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['front']