# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContactType'
        db.create_table(u'contacts_contacttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'contacts', ['ContactType'])

        # Adding M2M table for field sites on 'ContactType'
        m2m_table_name = db.shorten_name(u'contacts_contacttype_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contacttype', models.ForeignKey(orm[u'contacts.contacttype'], null=False)),
            ('site', models.ForeignKey(orm[u'sites.site'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contacttype_id', 'site_id'])

        # Adding model 'ContactTypeIcon'
        db.create_table(u'contacts_contacttypeicon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='icons', to=orm['contacts.ContactType'])),
            ('context', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'contacts', ['ContactTypeIcon'])

        # Adding unique constraint on 'ContactTypeIcon', fields ['type', 'context']
        db.create_unique(u'contacts_contacttypeicon', ['type_id', 'context'])

        # Adding model 'Contact'
        db.create_table(u'contacts_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_contact', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.ContactType'])),
        ))
        db.send_create_signal(u'contacts', ['Contact'])


    def backwards(self, orm):
        # Removing unique constraint on 'ContactTypeIcon', fields ['type', 'context']
        db.delete_unique(u'contacts_contacttypeicon', ['type_id', 'context'])

        # Deleting model 'ContactType'
        db.delete_table(u'contacts_contacttype')

        # Removing M2M table for field sites on 'ContactType'
        db.delete_table(db.shorten_name(u'contacts_contacttype_sites'))

        # Deleting model 'ContactTypeIcon'
        db.delete_table(u'contacts_contacttypeicon')

        # Deleting model 'Contact'
        db.delete_table(u'contacts_contact')


    models = {
        u'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_contact'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contacts.ContactType']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'contacts.contacttype': {
            'Meta': {'object_name': 'ContactType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'})
        },
        u'contacts.contacttypeicon': {
            'Meta': {'unique_together': "(('type', 'context'),)", 'object_name': 'ContactTypeIcon'},
            'context': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'icons'", 'to': u"orm['contacts.ContactType']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['contacts']