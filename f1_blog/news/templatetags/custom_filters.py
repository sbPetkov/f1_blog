from django.utils import timezone
from django import template
import datetime

register = template.Library()


@register.filter
def humanize_time(value):
    now = timezone.now()
    if isinstance(value, datetime.datetime):
        time_difference = now - value
        if time_difference < datetime.timedelta(hours=1):
            return f'Posted {time_difference.seconds // 60} minutes ago'
        elif time_difference < datetime.timedelta(days=1):
            return f'{time_difference.seconds // 3600} hours ago'
        else:
            return f'{time_difference.days} days ago'
    return value


