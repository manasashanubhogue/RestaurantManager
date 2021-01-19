from django.contrib import admin
from .models import (
    Address, 
    Menu, 
    MenuItem, 
    MenuItemType,
    Restaurant, 
    Review,
    User,
)

admin.site.register(Address)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(MenuItemType)
admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(User)
