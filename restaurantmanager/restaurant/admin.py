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
from import_export.admin import ImportExportModelAdmin
from restaurantmanager.restaurant import resources


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'phone_number')
    fieldsets = (
        ('Account Credentials', {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': (('first_name', 'last_name'), 'phone_number', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )
    class Meta:
        model = User


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_address', 'city', 'country')

    class Meta:
        model = Address


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Meta:
        model = Menu


class MenuItemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')

    class Meta:
        model = MenuItemType


class MenuItemAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price', 'restaurant')
    search_fields = ('restaurant__name',)

    resource_class = resources.MenuItemResource

    class Meta:
        model = MenuItem

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_verified', 'is_published')

    class Meta:
        model = Restaurant


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
