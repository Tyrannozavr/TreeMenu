from django.shortcuts import render
from .models import Menu, Item


def index(request, pk):
    # print(pk)
    pk = 0 if pk == '' else pk
    context = {'id': pk}
    return render(request, 'navigations/index.html', context=context)

