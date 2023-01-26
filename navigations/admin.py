from django.contrib import admin

from .models import *

admin.site.register(Menu)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['menu', 'name', 'parent']
