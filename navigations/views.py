from django.shortcuts import render
from .models import Menu, Item


def index(request):
    array = Item.objects.filter(menu__name='First menu')
    # obj = array.get(name='1.1.11')
    # array = get_tree(array, obj)
    # print('array is', array)
    context = {}
    context['name'] = [list(Menu.objects.all()) for i in range(3)]
    # print(context)
    return render(request, 'navigations/index.html', context=context)

