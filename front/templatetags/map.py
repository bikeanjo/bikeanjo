import json
from django import template
register = template.Library()


@register.filter(name='map')
def map(value, the_json):
    try:
        the_map = json.loads(the_json)
        return the_map.get(value, '')
    except:
        return ''
