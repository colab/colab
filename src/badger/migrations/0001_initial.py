# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Badge'
        db.create_table(u'badger_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('image_base64', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user_attr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('comparison', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100)),
        ))
        db.send_create_signal(u'badger', ['Badge'])

        # Adding M2M table for field awardees on 'Badge'
        m2m_table_name = db.shorten_name(u'badger_badge_awardees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('badge', models.ForeignKey(orm[u'badger.badge'], null=False)),
            ('user', models.ForeignKey(orm[u'accounts.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['badge_id', 'user_id'])

        # Adding model 'BadgeI18N'
        db.create_table(u'badger_badgei18n', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('i18n_language', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('i18n_source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['badger.Badge'])),
        ))
        db.send_create_signal(u'badger', ['BadgeI18N'])

        # Adding unique constraint on 'BadgeI18N', fields ['i18n_source', 'i18n_language']
        db.create_unique(u'badger_badgei18n', ['i18n_source_id', 'i18n_language'])


    def backwards(self, orm):
        # Removing unique constraint on 'BadgeI18N', fields ['i18n_source', 'i18n_language']
        db.delete_unique(u'badger_badgei18n', ['i18n_source_id', 'i18n_language'])

        # Deleting model 'Badge'
        db.delete_table(u'badger_badge')

        # Removing M2M table for field awardees on 'Badge'
        db.delete_table(db.shorten_name(u'badger_badge_awardees'))

        # Deleting model 'BadgeI18N'
        db.delete_table(u'badger_badgei18n')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'github': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'google_talk': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'verification_hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'webpage': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'badger.badge': {
            'Meta': {'ordering': "['order']", 'object_name': 'Badge'},
            'awardees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['accounts.User']", 'null': 'True', 'blank': 'True'}),
            'comparison': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_base64': ('django.db.models.fields.TextField', [], {}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_attr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'badger.badgei18n': {
            'Meta': {'unique_together': "(('i18n_source', 'i18n_language'),)", 'object_name': 'BadgeI18N'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'i18n_language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'i18n_source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['badger.Badge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['badger']