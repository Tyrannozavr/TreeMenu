from django import template
from navigations import models
from django.utils.safestring import mark_safe


register = template.Library()


@register.inclusion_tag('tags/hest.html')
def friend(name):
    return {'name': name}


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
    # print(item, type(item))
    # item = array.get(name='1')
    # print(2, item, type(item))
    lst = create_tree(array, item)
    menu = create_menu(lst)
    return mark_safe(menu)