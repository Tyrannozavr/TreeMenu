from django import template

register = template.Library()

def menu(value, arg):
    return value + arg

register.filter('menu', menu)
