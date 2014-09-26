# coding=utf-8
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .managers import ContactManager


class ContactType(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, null=True, blank=True)
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def icon(self, context):
        result = self.icons.filter(context=context) or []
        return result[0].icon if result else ""

    def __unicode__(self):
        return self.name


class ContactTypeIcon(models.Model):
    type = models.ForeignKey(ContactType, related_name='icons')
    context = models.CharField(max_length=20)
    icon = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s-%s" % (self.type.name, self.context)

    class Meta:
        unique_together = ('type', 'context')


class Contact(models.Model):
    # Content-object field
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    value = models.CharField(max_length=100)
    comments = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey(ContactType)

    objects = ContactManager()