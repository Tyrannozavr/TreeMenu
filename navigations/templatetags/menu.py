from django import template
from django.utils.safestring import mark_safe
from navigations import models

register = template.Library()


def create_tree(array, item, children=None):
    if not children:
        children = list(item.children_set.all())
    if not item.parents:
        parallel = list(array.filter(parents__isnull=True))
        parallel.insert(parallel.index(item) + 1, children)
        return parallel

    parallel = list(item.parents.children_set.all())
    parallel.insert(parallel.index(item) + 1, children)
    array = create_tree(array, item.parents, parallel)
    return array


def create_menu(lst):
    answer = []
    answer.append('<ul>')
    for i in lst:
        if type(i) is list:
            answer.append(create_menu(i))
        else:
            answer.append('<li>' + f'<a href="{i.id}">{i.name}</a>' + '</li>') if i else ''
    answer.append('</ul>')
    return ''.join(answer)

@register.simple_tag
def draw_menu(menu, active_id=None):
    array = models.Item.objects.filter(menu__name=menu)
    item = array.get(id=active_id) if active_id else array.first()
    lst = create_tree(array, item)
    menu = create_menu(lst)
    return mark_safe(menu)
