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
def dict_key(dictionary, key):
    """Fetch value from dictionary for the given key."""
    return dictionary.get(key, {})

@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except (TypeError, ValueError):
        return value
    

from datetime import timedelta
from datetime import datetime as dt  # Import datetime and alias it to avoid confusion

@register.filter
def subtract_hours(value, hours):
    """Subtract specified number of hours from a datetime."""
    if isinstance(value, dt):  # Use the alias here
        return value - timedelta(hours=hours)
    return value  # Return unchanged if not a datetime

@register.simple_tag
def year_range(start_year, end_year):
    return range(start_year, end_year + 1)


@register.filter
def generate_icons(infodetail, item):
    """
    Generate icons based on the count of a specific item in infodetail.
    Example: infodetail = '3 thé jetable', item = 'thé jetable'
    """
    infodetail = infodetail.lower() if infodetail else ''
    for part in infodetail.split(','):
        if item in part:
            try:
                count = int(part.split()[0])  # Extract the number
                return ''.join(
                    "<box-icon name='coffee-togo' color='#74C0FC' size='md'></box-icon>"
                    for _ in range(count)
                )
            except (IndexError, ValueError):
                pass
    return ''


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)




@register.filter
def render_mugs(infodetail):
    """
    Parses the number of 'thé thermos' from the string and returns a list of mug icons.
    Example: '2 thé thermos' -> 2 mugs
    """
    import re

    # Match patterns like '1 thé thermos', '2 thé thermos', etc.
    match = re.search(r'(\d+) thé thermos', infodetail.lower())
    if match:
        count = int(match.group(1))  # Extract the number
        return '<i class="fa-solid fa-mug-hot fa-2xl" style="color: #74C0FC;"></i> ' * count
    return ''


@register.filter
def render_mugscafe(infodetail):
    """
    Parses the number of 'café jetable' from the string and returns a list of mug icons.
    Example: '2 café jetable' -> 2 mugs
    """
    import re

    # Match patterns like '1 thé thermos', '2 thé thermos', etc.
    match = re.search(r'(\d+) café jetable', infodetail.lower())
    if match:
        count = int(match.group(1))  # Extract the number
        return " <box-icon name='coffee-togo' color='#533018' size='md'></box-icon> " * count
    return ''

@register.filter
def render_mugscafetherm(infodetail):
    """
    Parses the number of 'café jetable' from the string and returns a list of mug icons.
    Example: '2 café jetable' -> 2 mugs
    """
    import re

    # Match patterns like '1 thé thermos', '2 thé thermos', etc.
    match = re.search(r'(\d+) café thermos', infodetail.lower())
    if match:
        count = int(match.group(1))  # Extract the number
        return ' <i class="fa-solid fa-mug-hot fa-2xl" style="color: #533018;"></i> ' * count
    return ''


@register.filter
def contains_keyword(value, keyword):
    """
    Checks if the given keyword is present in the string (case-insensitive).
    """
    if not value:
        return False
    return keyword.lower() in value.lower()


@register.filter
def get_itemss(checklist_items, product_id):
    try:
        return checklist_items.get(product_id=product_id)
    except ChecklistItem.DoesNotExist:
        return None
    
@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})




@register.filter
def strip_zero_decimal(value):
    try:
        value = float(value)
        if value.is_integer():
            return int(value)
        return value
    except (ValueError, TypeError):
        return value
    

@register.filter
def sum_service_count(menu_submissions):
    return sum(int(submission.service_count or 0) for submission in menu_submissions)