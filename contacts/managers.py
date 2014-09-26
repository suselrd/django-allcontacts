# coding=utf-8
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text


class ContactManager(models.Manager):

    def for_object(self, obj):
        """
        QuerySet for all contacts for a particular object.
        """
        if not isinstance(obj, models.Model):
            raise Exception("model instance expected!")
        return self.get_queryset().filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=force_text(obj._get_pk_val())
        )