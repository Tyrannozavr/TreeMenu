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
    # print(request.path, request.GET, request.__dict__)
    # url = request.environ.get('HTTP_REFERER', '')
    # print(url)
    # print(request.path, '?', request.GET)
    path = request.path
    params = dict(request.GET)
    print(request.GET)
    if params.get(menu_name):
        params.pop(menu_name)
    print(params)
    params = ''.join([f'{key}={" ".join(value)}' for key, value in params.items()])
    url = path+'?'+params
    answer = []
    answer.append('<ul>')
    for i in lst:
        if type(i) is list:
            answer.append(create_menu(i, menu_name, context))
        else:
            new_arg = '&' + menu_name + '=' + str(i.id)
            answer.append('<li>' + f'<a href="{url+new_arg}">{i.name}</a>' + '</li>') if i else ''
            # answer.append('<li>' + f'<a href="?{menu_name}={i.id}">{i.name}</a>' + '</li>') if i else ''
    answer.append('</ul>')
    return ''.join(answer)

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
# def draw_menu(menu, active_id=None):
    menu = 'First menu'
    active_id = None
    # active_id = context['request'].path
    # print('draw', context['request'].path, menu_name)
    array = models.Item.objects.filter(menu__name=menu)
    item = array.get(id=active_id) if active_id else array.first()
    lst = create_tree(array, item)
    menu = create_menu(lst, menu_name, context)
    return mark_safe(menu)
