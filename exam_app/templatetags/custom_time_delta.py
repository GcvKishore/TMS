from django import template

register = template.Library()


@register.filter
def timeDelta(value):
    return str(value).split(".")[0]
