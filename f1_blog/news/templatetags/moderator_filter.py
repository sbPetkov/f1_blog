from django import template

register = template.Library()


@register.filter
def is_moderator_or_admin(user):
    return user.groups.filter(name='moderator').exists() or user.is_staff
