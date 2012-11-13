from mezzanine import template
from mezzanine_recipes.fields import DIFFICULTIES, UNITS

register = template.Library()

@register.simple_tag
def get_difficulty_name(object):
    return dict(DIFFICULTIES)[object.difficulty]

@register.simple_tag
def get_unit_name(object):
    return dict(UNITS)[object.unit]

@register.simple_tag
def get_time_period(object):
    period = "%02d:%02d" %(object.hours, object.minutes)
    if hasattr(object, 'days'):
        period = "%02d:%s" %(object.days, period)
    return period
