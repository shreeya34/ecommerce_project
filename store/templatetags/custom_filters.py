# store/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def abs_filter(value):
    return abs(value)