from django.shortcuts import render

from .models import Item, Menu


def index(request, pk):
    pk = 0 if pk == '' else pk
    context = {'id': pk}
    return render(request, 'navigations/index.html', context=context)

