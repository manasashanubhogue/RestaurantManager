from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render
from restaurantmanager.restaurant.models import (
    Address, Restaurant, User, MenuItem, Review )
from restaurantmanager.restaurant.utils import (
    has_permission_to_manage_restaurant,
    has_permission_to_edit_restaurant,
    is_restaurant_manager,
    validate_params,
    get_menu_and_item_type)

class UserDetailsAPI(viewsets.ViewSet):

    #TODO: handle validation of email/ph, loggers
    @validate_params({'email': str, 'first_name': str, 'last_name': str, 'password': str})
    def create_user(self, request):
        """ Function to create user for the application
        request_data: user detail dict , sample dictionaries in mock_data/users.json"""
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = make_password(request.data.get('password'))
        phone_number = request.data.get('phone_number', None)
        try:
            User.objects.create(is_staff=False,
                is_active=True, email=email, username=email, first_name=first_name,
                last_name=last_name, password=password, phone_number=phone_number)
            return Response(data="User created sucessfully")
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Email already exists"})

    def get_app_users(self, request):
        """ Func to get list of emails as dropdown
        Use: Add restaurant API, to assign value to manager field"""
        current_user = request.user
        # all user emails are displayed for admin, and only self for restaurant managers
        if current_user.is_superuser:
            user_list = User.get_user()
        else:
            user_list = User.get_user(current_user.id)
        return Response(user_list)

class RestaurantDetailsAPI(viewsets.ViewSet):

    def __init__(self):
        self.all_fields = ['id', 'name', 'address__full_address', 'address__city', 'address__country',
                            'url', 'phone_number', 'opening_time', 'closing_time', 'is_published', 'manager_id']

    def restaurant_meta_data(self, request):
        """ fetch all restaurants - to display in home page """
        restaurants = Restaurant.get_restaurant_data({}, values=[*self.all_fields])
        return Response(restaurants)

    def add_restaurant_details(self, request):
        """ Add new restaurant details and return restaurants managed by user
        request_data: list of restaurant dicts, sample list in mock_data/restaurants.json
        """
        user = request.user
        request_data_list = request.data
        filter_param = {}
        # loop through and create address obj and use that to create restaurant obj
        for each_dict in request_data_list:
            address = each_dict['address']
            address_obj, created = Address.objects.get_or_create(full_address=address['full_address'],
                city=address['city'], country=address['country'])
            each_dict.update({'address': address_obj})
        Restaurant.bulk_save_dicts(request_data_list)
        # on addition, return all restaurants managed by current user, else return all if admin
        if not user.is_superuser:
            filter_param = {Q(manager=user.id)}
        response_data = Restaurant.get_restaurant_data(filter_param, values=[*self.all_fields])
        return Response(data=response_data, message='Creation successfull')

    def get_my_dashboard_data(self, filter_param):
        # restaurants that are verified by admin and published by manager
        live = Restaurant.get_restaurant_data({filter_param & Q(is_published=True, is_verified=True)}, values=[*self.all_fields])
        # restaurants that are published by manager and sent for verification
        in_progress = Restaurant.get_restaurant_data({filter_param & Q(is_published=True) & Q(is_verified=False)}, values=[*self.all_fields])
        # restaurants that are added by not yet published by manager
        in_draft = Restaurant.get_restaurant_data({filter_param & Q(is_published=False) & Q(is_verified=False)}, values=[*self.all_fields])
        response_data = {
            'Published Restaurants': live,
            'To be Verified': in_progress,
            'Draft': in_draft
        }
        return response_data

    def manage_restaurant_details(self, request):
        """ Method to show restaurants managed by user with filters """
        current_user = request.user
        # page is visible to admin and restaurant managers
        has_permission, filter_param = has_permission_to_manage_restaurant(current_user)
        if has_permission:
            response_data = self.get_my_dashboard_data(filter_param)
            return Response(data=response_data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "You are not authorized to do this action"})

    def edit_restaurant_details(self, request, restaurant_id):
        """ Update restaurant related details """
        current_user = request.user
        request_data = request.data
        has_permission = has_permission_to_edit_restaurant(current_user, restaurant_id)
        input_dict = dict()
        if has_permission:
            address_obj, created = Address.objects.get_or_create(full_address=request_data['address__full_address'],
                city=request_data['address__city'], country=request_data['address__country'])
            input_dict.update({
                'name': request_data['name'],
                'address_id': address_obj.id,
                'url': request_data['url'],
                'phone_number': request_data['phone_number'],
                'opening_time': request_data['opening_time'],
                'closing_time': request_data['closing_time'],
                'is_published': request_data['is_published'],
                'manager_id': request_data['manager_id']
            })
            Restaurant.objects.filter(id=restaurant_id).update(**input_dict)
            response_data = Restaurant.get_restaurant_data({Q(id=restaurant_id)}, values=[*self.all_fields])
            return Response(response_data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "You are not authorized to do this action"})

    def update_restaurant_verification(self, request):
        """ Method to mark restaurant as verified, returns restaurant dashboard data """
        restaurant_id = request.data.get('restaurant_id')
        if request.user.is_superuser:
            restaurant_obj = Restaurant.objects.filter(id=restaurant_id).update(is_verified=True)
            return Response(data=self.get_my_dashboard_data(Q()))
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "You are not authorized to do this action"})


    def get_restaurant_details(self, request, restaurant_id):
        """ given id return restaurant menu n review details """
        menu_details = MenuItem.get_restaurant_menu(restaurant_id)
        reviews = Review.get_review_by_restaurant(restaurant_id)
        # reviews = sorted(reviews, key=lambda review: review['rating'])
        response_data = {
            'menu': menu_details,
            'reviews': reviews
        }
        return Response(data=response_data)

class MenuDetailsAPI(viewsets.ViewSet):

    def get_menu_types(self, request):
        """ Method to return menu and types - dropdown data required to add menu """
        menu_item_type, menu = get_menu_and_item_type()
        cuisine_type = {x:y for (x, y) in MenuItem.CUISINES_CHOICES}
        response_data = {
            'menu_item': menu_item_type,
            'menu': menu,
            'cuisine': cuisine_type.keys()
        }
        return Response(data=response_data)


    @validate_params({'name': str, 'menuitemtype': int, 'menu_category': int, 'description': str,
    'price': float, 'menu_item_id': int})
    def add_update_menu_item(self, request, restaurant_id):
        """ Method to add restaurant menu - only done by manager,
        menu, menu item, cusine data needed is sent via meta data call """
        # given restaurant id - verify if he is manager and retaurant exists
        if is_restaurant_manager(request.user, restaurant_id):
            request_data = request.data
            menu_item_id = request_data.get('menu_item_id')
            menu_dict = {
                'name': request_data.get('name'),
                'menu_item_type_id': request_data.get('menuitemtype'),
                'menu_id': request_data.get('menu_category'),
                'restaurant_id': restaurant_id,
                'description': request_data.get('description'),
                'price': request_data.get('price'),
                'type': request_data.get('cuisine_type')
            }
            # if menu_id is -1 => new menu else perform menu edit
            if menu_item_id > 0:
                menu_item_obj = MenuItem.objects.filter(id=menu_item_id)
                menu_item_obj.update(**menu_dict)
            else:
                MenuItem.objects.create(**menu_dict)
            # returns all menu items of the restaurant
            return Response(MenuItem.get_restaurant_menu(restaurant_id))
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "You are not authorized to do this action"})

class ReviewAPI(viewsets.ViewSet):

    @validate_params({'rating': int, 'comment': str})
    def add_update_review(self, request, restaurant_id):
        """ """
        request_data = request.data
        current_user = request.user.id
        try:
            review_id = request_data.get('review_id')
            review_dict = {
                'rating': request_data.get('rating'),
                'comment': request_data.get('comment'),
                'reviewer': request.user,
                'restaurant_id':restaurant_id
            }
            # if review_id is -1, create an obj else update
            if review_id > 0:
                review_obj = Review.objects.filter(id=review_id, reviewer=current_user)
                review_obj.update(**review_dict)
            else:
                Review.objects.create(**review_dict)
            return Response(data="Review has been Successfully updated")
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Review already exists"})
