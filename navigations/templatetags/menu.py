from django import template
from django.db.models import Q
from django.utils.safestring import mark_safe
from navigations.models import Item

register = template.Library()


def create_tree(array, item, children=None):
    """
    :param array: contains all elements, needed to create tree menu
    :param item: current item in this menu
    :param children: this parameter is needed for the recursion to work correctly
    :return: nested list, where the deepest list contains current element or its children.
     Or one list with top level elements.
     """
    if not children:
        children = list(item.children_set.all())
    if not item.parent:
        parallel = list(array.filter(parent__isnull=True))
        parallel.insert(parallel.index(item) + 1, children)
        return parallel

    parallel = list(item.parent.children_set.all())
    parallel.insert(parallel.index(item) + 1, children)
    array = create_tree(array, item.parent, parallel)
    return array


def create_menu(lst, menu_name, request):
    """
    this function wraps a nested list of elements, turning it into
     a ready-made html list consisting of links with the preservation of parameters and leading to child elements.
     Hierarchy in link necessary for making single request in DB.
    :param lst: is nested list elements for menu
    :param menu_name: needed for creating correct link parameters on elements tree
    :param request: contains path and old parameters who could be saving
    :return: html code tree menu
    """
    path = request.path
    params = dict(request.GET)
    if params.get(menu_name):
        params.pop(menu_name)
    params = ''.join([f'{key}={" ".join(value)}' for key, value in params.items()])  # external params look like list
    url = path + '?' + params
    answer = ['<ul>']
    for i in lst:
        if type(i) is list:  # recursion on  child elements
            answer.append(create_menu(i, menu_name, request))
        else:  # creating html elements for a list
            if i.hierarchy:
                hierarchy = str(i.id) + ':' + i.hierarchy
            else:
                hierarchy = str(i.id)
            new_arg = menu_name + '=' + hierarchy
            if url[-1] != '?':  # it's necessary for saving external parameters
                new_arg = '&' + new_arg
            answer.append('<li>' + f'<a href="{url + new_arg}">{i.name}</a>' + '</li>') if i else ''
    answer.append('</ul>')
    return ''.join(answer)


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    """
    :param context: contains named arguments (optional) view: menu_name=id (one id, or set of ids look like "id1:id2..."
    :param menu_name: string
    :return: ready menu, html code
    """
    request = context['request']
    active_ids = request.GET.get(menu_name)
    if isinstance(active_ids, int):  # active ids might look like one id (number)
        current_id = int(active_ids)
    elif active_ids:
        # or look like  'id1:id2:id3' first argument is current element, others are his parents
        active_ids = [int(i) for i in active_ids.split(':')]
        current_id = active_ids[0]
    else:  # and finally may don't have arguments
        tree = Item.objects.filter(menu__name=menu_name, parent__isnull=True)
        menu = create_menu(tree, menu_name, request)
        return mark_safe(menu)

    array = Item.objects \
        .filter(Q(menu__name=menu_name, id__in=active_ids) | Q(menu__name=menu_name, parent__isnull=True))
    current_item = array.get(id=current_id)
    tree = create_tree(array, current_item)
    menu = create_menu(tree, menu_name, request)
    return mark_safe(menu)
