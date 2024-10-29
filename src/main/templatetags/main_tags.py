import os
from django import template
from django.utils.http import urlencode
from django.utils import translation
from bs4 import BeautifulSoup
import humanize
import bleach


register = template.Library()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.filter
def clear_tags(value):
    text = BeautifulSoup(value, 'html.parser')
    return text.get_text()


@register.filter
def bleach_linkify(value):
    return bleach.clean(value)


@register.filter
def basename(value):
    return os.path.basename(value)


@register.filter
def humanize_naturaltime(value):
    humanize.i18n.activate(translation.get_language())
    time = humanize.naturaltime(value)
    return time
