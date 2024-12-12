# your_app/templatetags/custom_filters.py
from django import template
from listings.models import ChecklistItem

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)

@register.filter(name='status_color')
def status_color(status):
    color_map = {
        'en_cours': '#ff9800',  # orange
        'valide': '#4caf50',    # green
        'refuse': '#f44336',    # red
    }
    return color_map.get(status, '#000')  # Default to black if status is not in map

@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except (TypeError, ValueError):
        return value
    

@register.simple_tag
def year_range(start_year, end_year):
    return range(start_year, end_year + 1)