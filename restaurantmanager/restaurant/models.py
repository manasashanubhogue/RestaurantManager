from django.db import models
from django.core.validators import RegexValidator
from django.db.models.fields import FloatField

class Address(models.Model):
    full_address = models.CharField(max_length=1024)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class Restaurant(models.Model):
    """ Model to store restaurant details """
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, related_name='location', on_delete=models.CASCADE)
    url = models.URLField(max_length=200, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    opening_time = models.TimeField(auto_now=False, auto_now_add=False)
    closing_time = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name
    
    class Meta: # new
        indexes = [models.Index(fields=['name'])]
        ordering = ['-name']
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'


class Menu(models.Model):
    """ Model to store Menu - Food/bar"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

class MenuItemType(models.Model):
    """ Model to store menu item types """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024) 

    def __str__(self):
        return self.name   

class MenuItem(models.Model):
    """ Model to store menu item """
    name = models.CharField(max_length=100)
    menu_item_type = models.ForeignKey(MenuItemType, on_delete=models.CASCADE, related_name='menu_type')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_category')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_menu')
    description = models.CharField(max_length=1024)
    price = models.FloatField()

    def __str__(self):
        return '%s-%s'% (self.name, self.restaurant.name)
    
