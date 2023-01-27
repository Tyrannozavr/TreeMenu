from django.contrib import admin
from django import forms
from .widgets import Tags
from .models import *


# admin.site.register(Menu)

class ItemInline(admin.StackedInline):
    model = Item
    extra = 1
    fields = ('name', 'parent')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ function for creating items using admin panel, field parents contains only items current menu"""
        if db_field.name == 'parent':
            menu_id = request.resolver_match.kwargs.get('object_id')
            kwargs['queryset'] = Item.objects.filter(menu_id=menu_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = (ItemInline,)
    fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['menu', 'name', 'parent']
   # def formfield_for_foreignkey(self, db_field, request, **kwargs):
   #      if db_field.name == "parent":
   #          kwargs["queryset"] = self.objects.get_complete_queryset()
   #      return super().formfield_for_foreignkey(db_field, request, **kwargs)
   #
   #  # formfield_overrides = {
   #  #     models.ForeignKey: {'widget': Tags},
   #  # }