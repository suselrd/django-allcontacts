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
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Description'))
    sites = models.ManyToManyField(Site, _('Sites'))

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        verbose_name = _('Contact Type')
        verbose_name_plural = _('Contact Types')

    def icon(self, context):
        result = self.icons.filter(context=context) or []
        return result[0].icon if result else ""

    def __unicode__(self):
        return u"%s" % self.name


class ContactTypeIcon(models.Model):
    type = models.ForeignKey(ContactType, related_name='icons', verbose_name=_('Type'))
    context = models.CharField(max_length=20, verbose_name=_('Context'))
    icon = models.CharField(max_length=20, verbose_name=_('Icon'))

    def __unicode__(self):
        return u"%s-%s" % (self.type, self.context)

    class Meta:
        unique_together = ('type', 'context')


class Contact(models.Model):
    # Content-object field
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('Content Type'),
                                     related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('Object ID'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    content_type_label = models.CharField(max_length=255, blank=True, verbose_name=_('Contact Type Label'))

    value = models.CharField(max_length=100, verbose_name=_('Value'))
    comments = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Comments'))
    type = models.ForeignKey(ContactType, verbose_name=_('Type'))

    objects = ContactManager()

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


@receiver(pre_save, sender=Contact, dispatch_uid='contact_pre_save')
def contact_pre_save_handler(instance, raw, **kwargs):
    if instance.content_type_id:
        instance.content_type_label = ".".join(ContentType.objects.get(pk=instance.content_type_id).natural_key())
    if not instance.content_type_id and instance.content_type_label:
        app_label, model = instance.content_type_label.split('.')
        instance.content_type = ContentType.objects.get_by_natural_key(app_label, model)