from django import template

register = template.Library()

def get_type(value):
    return type(value)


register.filter('get_type', get_type)
