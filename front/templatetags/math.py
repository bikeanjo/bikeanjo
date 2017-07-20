import re
from django import template
register = template.Library()


def return_numbers(*args):
    values = []
    for arg in args:
        if type(arg) in (float, int,):
            values.append(arg)
        elif type(arg) is str:
            if arg.isdigit():
                values.append(int(arg))
            elif re.match('^\d+(\.\d+)?$', arg):
                values.append(float(arg))
    return values


@register.simple_tag(name='min')
def minvalue(*args):
    values = return_numbers(*args)
    if len(values) > 0:
        return min(values)
    return ''


@register.simple_tag(name='max')
def maxvalue(*args):
    values = return_numbers(*args)
    if len(values) > 0:
        return max(values)
    return ''
