from django import template
from datetime import timedelta, datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def add_hour(time_obj, hours):
    # Create a dummy datetime object to perform the addition
    dummy_date = datetime.combine(datetime.min, time_obj)
    new_time = (dummy_date + timedelta(hours=hours)).time()
    return new_time
