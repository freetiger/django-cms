# -*- coding: utf-8 -*-
import json
import warnings

from classytags.core import Tag, Options
from cms.utils.encoder import SafeJSONEncoder
from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.text import javascript_quote
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def js(value):
    warnings.warn("The template filter '...|js' is vulnerable to XSS attacks, please use '...|json' instead.",
                  DeprecationWarning, stacklevel=2)
    return json.dumps(value, cls=DjangoJSONEncoder)


@register.filter('json')
def json_filter(value):
    """
    Returns the JSON representation of ``value`` in a safe manner.
    """
    return mark_safe(json.dumps(value, cls=SafeJSONEncoder))


@register.filter
def bool(value):
    if value:
        return 'true'
    else:
        return 'false'


class JavascriptString(Tag):
    name = 'javascript_string'
    options = Options(
        blocks=[
            ('end_javascript_string', 'nodelist'),
        ]
    )

    def render_tag(self, context, **kwargs):
        rendered = self.nodelist.render(context)
        return u"'%s'" % javascript_quote(rendered.strip())
register.tag(JavascriptString)
