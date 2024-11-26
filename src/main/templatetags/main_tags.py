import os
from datetime import datetime, date
from django import template
from django.utils import translation
from django.utils.http import urlencode
from bs4 import BeautifulSoup
import humanize
import bleach


register = template.Library()
months_ukr = [
    'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
    'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'
]


@register.filter
def month(value):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return value

    if isinstance(value, (datetime, date)):
        return f'{value.day} {months_ukr[value.month - 1]}'


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.filter
def get_item(dictionary: dict, key: str):
    return dictionary.get(key, None)


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
