# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MessageBlock'
        db.create_table(u'super_archives_messageblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blocks', to=orm['super_archives.Message'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('is_reply', self.gf('django.db.models.fields.BooleanField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'super_archives', ['MessageBlock'])


    def backwards(self, orm):
        # Deleting model 'MessageBlock'
        db.delete_table(u'super_archives_messageblock')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'google_talk': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'super_archives.emailaddress': {
            'Meta': {'ordering': "('id',)", 'object_name': 'EmailAddress'},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'real_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['accounts.User']"})
        },
        u'super_archives.emailaddressvalidation': {
            'Meta': {'unique_together': "(('user', 'address'),)", 'object_name': 'EmailAddressValidation'},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails_not_validated'", 'null': 'True', 'to': u"orm['accounts.User']"}),
            'validation_key': ('django.db.models.fields.CharField', [], {'default': "'f7c4c15797f34834bf5a8b9bd84fabee'", 'max_length': '32', 'null': 'True'})
        },
        u'super_archives.keyword': {
            'Meta': {'ordering': "('?',)", 'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': "'128'"}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.Thread']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'super_archives.mailinglist': {
            'Meta': {'object_name': 'MailingList'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_imported_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'super_archives.mailinglistmembership': {
            'Meta': {'object_name': 'MailingListMembership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.MailingList']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'super_archives.message': {
            'Meta': {'ordering': "('received_time',)", 'unique_together': "(('thread', 'message_id'),)", 'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'from_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.EmailAddress']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'received_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'spam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512', 'db_index': 'True'}),
            'subject_clean': ('django.db.models.fields.CharField', [], {'max_length': '512', 'db_index': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.Thread']", 'null': 'True'})
        },
        u'super_archives.messageblock': {
            'Meta': {'ordering': "('order',)", 'object_name': 'MessageBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reply': ('django.db.models.fields.BooleanField', [], {}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blocks'", 'to': u"orm['super_archives.Message']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'super_archives.messagemetadata': {
            'Message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.Message']"}),
            'Meta': {'object_name': 'MessageMetadata'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'super_archives.pagehit': {
            'Meta': {'object_name': 'PageHit'},
            'hit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        u'super_archives.thread': {
            'Meta': {'unique_together': "(('subject_token', 'mailinglist'),)", 'object_name': 'Thread'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_message': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': u"orm['super_archives.Message']"}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.MailingList']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'spam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_token': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'super_archives.vote': {
            'Meta': {'unique_together': "(('user', 'message'),)", 'object_name': 'Vote'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.Message']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        }
    }

    complete_apps = ['super_archives']