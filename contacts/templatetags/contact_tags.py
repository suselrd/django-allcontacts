# coding=utf-8
from django import template
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.assignment_tag
def contact_icon(obj, context):
    """
    Gets the proper icon to display with a contact item in a given context

    Syntax::

         {% contact_icon [obj] [context] as [name] %}
    """
    from ..models import Contact
    if not obj:
        return ""
    if not isinstance(obj, Contact):
        raise Exception(_("The object must be a contact instance"))
    return force_text(obj.type.icon(context))