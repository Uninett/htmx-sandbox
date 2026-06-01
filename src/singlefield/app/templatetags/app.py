from django import template


register = template.Library()


@register.filter
def by_key(d, k):
    return d.get(k, '')
