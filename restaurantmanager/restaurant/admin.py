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

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'phone_number')

    class Meta:
        model = User

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_address', 'city', 'country')

    class Meta:
        model = Address
        ordering = ['pk']

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Meta:
        model = Menu
        ordering = ['pk']

class MenuItemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')

    class Meta:
        model = MenuItemType
        ordering = ['pk']

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'restaurant')
    search_fields = ('restaurant__name',)

    class Meta:
        model = MenuItem
        ordering = ['pk']

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_verified', 'is_published')

    class Meta:
        model = Restaurant
        ordering = ['pk']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'rating', 'comment', 'reviewer', 'last_updated')
    readonly_fields = ('last_updated', 'restaurant', 'rating', 'comment', 'reviewer',)

    class Meta:
        model = Review

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

admin.site.register(Address, AddressAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(MenuItemType, MenuItemTypeAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(User, UserAdmin)
