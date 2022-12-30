from django.shortcuts import render
from .models import Menu, Item

# def get_parents()

# def get_tree(array, item):
#     # print(array, item, 'par', item.parents)
#     # print(bool(item.parents))
#     if item.parents:
#         new_array = list(item.parents.children_set.all())
#         middle = get_tree(array, item.parents)
#         # print(new_array, middle, item.parents)
#         middle.insert(middle.index(item.parents)+1, new_array)
#         new_array = middle
#         return new_array
#     else:
#         new_array = list(array.filter(parents__isnull=True))
#         return new_array

def get_tree(array, item, children=None):
    if not item.parents:
        parallel = list(array.filter(parents__isnull=True))
        parallel.insert(parallel.index(item)+1, children)
        # print(parallel, '\t', children)
        print(parallel)
        return parallel

    childrens = list(item.children_set.all())
    parallel = list(item.parents.children_set.all())
    parallel.insert(parallel.index(item)+1, childrens)
    get_tree(array, item.parents, parallel)


def index(request):
    array = Item.objects.filter(menu__name='First menu')
    # print(array, array.get(name='1.1.11'))
    obj = array.get(name='1.1.11')
    # print(obj)
    # print('parent is', obj.parents)
    print('result', get_tree(array, obj))
    context = {}
    context['name'] = [list(Menu.objects.all()) for i in range(3)]
    return render(request, 'navigations/index.html', context=context)

