# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, ModelChoiceField
from .models import Contact, ContactType


class ContactForm(ModelForm):
    type = ModelChoiceField(queryset=ContactType.on_site.all(), empty_label=_(u"--Type (*)--"))

    class Meta:
        model = Contact
        fields = ('value', 'type', "comments")
