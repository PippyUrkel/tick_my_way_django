# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})

@register.filter(name='attr')
def attr(value, args):
    attrs = {}
    for arg in args.split(','):
        key, val = arg.split(':')
        attrs[key] = val
    return value.as_widget(attrs=attrs)