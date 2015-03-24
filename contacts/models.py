# coding=utf-8
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
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

    content_type_label = models.CharField(max_length=255, blank=True)

    value = models.CharField(max_length=100)
    comments = models.CharField(max_length=100, null=True, blank=True)
    type = models.ForeignKey(ContactType)

    objects = ContactManager()


@receiver(pre_save, sender=Contact, dispatch_uid='contact_pre_save')
def contact_pre_save_handler(instance, raw, **kwargs):
    if instance.content_type_id:
        instance.content_type_label = ".".join(ContentType.objects.get(pk=instance.content_type_id).natural_key())
    if not instance.content_type_id and instance.content_type_label:
        app_label, model = instance.content_type_label.split('.')
        instance.content_type = ContentType.objects.get_by_natural_key(app_label, model)