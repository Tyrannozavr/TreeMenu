from django.contrib import admin
from django import forms

from .models import *


# admin.site.register(Menu)

class ItemInline(admin.StackedInline):
    model = Item
    extra = 1
    fields = ('name', 'parent')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = (ItemInline,)
    fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['menu', 'name', 'parent']
