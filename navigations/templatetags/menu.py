from django import template

register = template.Library()

@register.inclusion_tag('tags/menu.html')
def draw_menu(value):
    return value.capitalize()


@register.inclusion_tag('tags/results.html')
def show_results(poll):
    choices = poll
    return {'choices': choices}
