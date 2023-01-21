from django.contrib import admin

from .models import *

admin.site.register(Menu)
# admin.site.register(Item)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['menu', 'name', 'parents']
