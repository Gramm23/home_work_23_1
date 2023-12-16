from django import template
from django.conf import settings

register = template.Library()


@register.filter
def image_path(image_field):
    full_path = settings.MEDIA_URL + str(image_field)
    return full_path



