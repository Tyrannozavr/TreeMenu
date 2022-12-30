from django.shortcuts import render
from .models import Menu, Item


def get_tree(array, item, children=None):
    if not item.parents:
        parallel = list(array.filter(parents__isnull=True))
        parallel.insert(parallel.index(item)+1, children)
        return parallel

    childrens = list(item.children_set.all())
    parallel = list(item.parents.children_set.all())
    parallel.insert(parallel.index(item)+1, childrens)
    array = get_tree(array, item.parents, parallel)
    return array




def index(request):
    array = Item.objects.filter(menu__name='First menu')
    obj = array.get(name='1.1.11')
    array = get_tree(array, obj)
    # print('array is', array)
    context = {}
    context['name'] = [list(Menu.objects.all()) for i in range(3)]
    print(context)
    return render(request, 'navigations/index.html', context=context)

