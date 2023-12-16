from django import template

from product.templatetags.filters import image_path

register = template.Library()


@register.simple_tag
def media_path(image_field):
    return image_path(image_field)



