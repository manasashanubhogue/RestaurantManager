from django.contrib import admin
from .models import Address, Restaurant, Menu, MenuItem, MenuItemType


admin.site.register(Address)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(MenuItemType)
