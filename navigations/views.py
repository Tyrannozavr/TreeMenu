from django.shortcuts import render
from .models import Menu, Item

# def get_parents()

def get_tree(array, item):
    # print(array, item, 'par', item.parents)
    # print(bool(item.parents))
    if item.parents:
        new_array = list(item.parents.children_set.all())
        middle = get_tree(array, item.parents)

        print(new_array, ':', middle, ':', item)
        # middle.insert(middle.index(item.parents)+1, new_array)
        # new_array.insert(new_array.index(item)+1, get_tree(array, item.parents))

        return new_array
    else:
        new_array = list(array.filter(parents__isnull=True))
        # print('null', new_array)
        return new_array

def index(request):
    array = Item.objects.filter(menu__name='First menu')
    # print(array, array.get(name='1.1.11'))
    obj = array.get(name='1.1.11')
    # print(obj)
    # print('parent is', obj.parents)
    array = get_tree(array, obj)
    print('itog', array)
    context = {}
    context['name'] = [list(Menu.objects.all()) for i in range(3)]
    return render(request, 'navigations/index.html', context=context)

