from django import template

register = template.Library()


@register.filter
def inc(value, add_value):
    return int(float(value)) + int(float(add_value))


@register.simple_tag
def division(a, b, to_int=False):
    if to_int == True:
        return int(float(a) / float(b))
    else:
        return float(a) / float(b)

