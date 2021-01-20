from django.db import models
from django.db.models import F
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import FloatField


class User(AbstractUser):
    """Class to store User info."""

    AbstractUser._meta.get_field("username").max_length = 255
    AbstractUser._meta.get_field("first_name").max_length = 255
    AbstractUser._meta.get_field("last_name").max_length = 255
    temp_password = models.CharField(max_length=255, null=True, blank=True) # use for reset password email functionality
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        """Meta Data."""
        verbose_name = 'App User'
        verbose_name_plural = 'App Users'

    def __str__(self):
        """String representation of the model."""
        return self.username

    @classmethod
    def get_user(cls, user_id=None):
        """ Return user email based on id """
        user_objs = cls.objects
        if user_id:
            user_objs = user_objs.filter(id=user_id)
        return user_objs.values('email', 'id')


class BaseModel():

    @classmethod
    def bulk_save_dicts(cls, list_of_dicts=[]):
        """Save dicts to table."""

        bulk_create_obj_list = []
        for each_dict in list_of_dicts:
            each_obj = cls(**each_dict)
            bulk_create_obj_list.append(each_obj)

        cls.objects.bulk_create(bulk_create_obj_list)

    @classmethod
    def bulk_delete(cls, filter_param={}):
        """Delete all objects from the table."""

        cls.objects.filter(**filter_param).delete()

class Address(models.Model):
    """ Model to store address of restaurants """
    full_address = models.CharField(max_length=1024)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.full_address)

    class Meta:
        unique_together = ('full_address', 'city', 'country',)

class Restaurant(BaseModel, models.Model):
    """ Model to store restaurant details """
    name = models.CharField(max_length=100, unique=True)
    address = models.ForeignKey(Address, related_name='location', on_delete=models.CASCADE)
    url = models.URLField(max_length=200, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    opening_time = models.TimeField(auto_now=False, auto_now_add=False)
    closing_time = models.TimeField(auto_now=False, auto_now_add=False)
    is_verified = models.BooleanField(default=False) # app admin can only verify
    is_published = models.BooleanField(default=False) # restaurant is published on verification, post verification, restaurnat managers can disbale
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_manager')

    def __str__(self):
        return self.name

    @classmethod
    def get_restaurant_data(cls, filter_param={}, values=[]):
        """ Returns restaurants based on filters and values requested"""
        restaurants = cls.objects.filter(*filter_param)
        if values:
            restaurants = restaurants.values(*values)
        return restaurants


class Menu(models.Model):
    """ Model to store Menu - Breakfast/Dinner/Drinks"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)  # note-availability

    def __str__(self):
        return self.name


class MenuItemType(models.Model):
    """ Model to store menu item types - Appetizers, Mocktails, .."""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name   


class MenuItem(models.Model):
    """ Model to store menu item """
    CUISINES_CHOICES = (
		('NA', 'NONE'),
		('VEGAN', 'Vegan'),
		('VEGETARIAN', 'Vegetarian'),
	)

    name = models.CharField(max_length=100)
    menu_item_type = models.ForeignKey(MenuItemType, on_delete=models.CASCADE, related_name='menu_type')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_category')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_menu')
    description = models.CharField(max_length=1024) #contents
    price = models.FloatField()
    type = models.CharField(max_length=15, choices=CUISINES_CHOICES, default='NA')

    def __str__(self):
        return '%s-%s'% (self.name, self.restaurant.name)
    

class Review(models.Model):
    """ Model to store reviews for restaurants """
    RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    rating = models.IntegerField(blank=False, default=3,choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_reviewer')
    last_updated = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_reviewed')