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


def create_menu(lst, menu_name, context):
    request = context['request']
    path = request.path
    params = dict(request.GET)
    if params.get(menu_name):
        params.pop(menu_name)
    params = ''.join([f'{key}={" ".join(value)}' for key, value in params.items()])
    url = path+'?'+params
    answer = []
    answer.append('<ul>')
    for i in lst:
        if type(i) is list:
            answer.append(create_menu(i, menu_name, context))
        else:
            if url[-1] == '?':
                new_arg = menu_name + '=' + str(i.id)
                answer.append('<li>' + f'<a href="{url+new_arg}">{i.name}</a>' + '</li>') if i else ''
            else:
                new_arg = '&' + menu_name + '=' + str(i.id)
                answer.append('<li>' + f'<a href="{url+new_arg}">{i.name}</a>' + '</li>') if i else ''
    answer.append('</ul>')
    return ''.join(answer)

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    active_id = request.GET.get(menu_name)
    # print(active_id, type(active_id))
    hierarchy = models.Item.objects.get(id=active_id).hierarchy
    ids = list(map(int, [active_id, *hierarchy.split('.')]))
    print(ids)

    if not active_id:
        lst = models.Item.objects.filter(menu__name=menu_name, parents=None)
        menu = create_menu(lst, menu_name, context)
        return mark_safe(menu)
    array = models.Item.objects.filter(menu__name=menu_name)
    item = array.get(id=active_id)
    lst = create_tree(array, item)
    menu_name = create_menu(lst, menu_name, context)
    return mark_safe(menu_name)
