import re
from django.shortcuts import render
from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from restaurantmanager.restaurant.models import Address, Restaurant, User
from restaurantmanager.restaurant.utils import (
    has_permission_to_manage_restaurant,
    has_permission_to_edit_restaurant )

class UserDetailsAPI(viewsets.ViewSet):
     
    #TODO: handle validation of email/ph, loggers
    # @validate_params({'email': str, 'first_name': str, 'last_name': str, 'password': str})
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
        self.all_fields = ['id', 'name', 'address__full_address',
                            'url', 'phone_number', 'opening_time', 'closing_time']

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
        return Response(data=response_data)

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

    def edit_restaurant_details(self, request):
        """ Update restaurant related details"""
        current_user = request.user
        restaurant_id = request.data.get('restaurant_id')
        has_permission = has_permission_to_edit_restaurant(current_user, restaurant_id)
        if has_permission:
            pass
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "You are not authorized to do this action"})
 
    def update_restaurant_verification(self, request):
        """ Method to mark restaurant as verified """
        restaurant_id = request.data.get('restaurant_id')
        if request.user.is_superuser:
            restaurant_obj = Restaurant.objects.filter(id=restaurant_id).update(is_verified=True)
            return Response(data=self.get_my_dashboard_data(Q()))
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": "You are not authorized to do this action"})


    def get_restaurant_details(self, request):
        """ given id return menu, reviews as 2 dict inside (nested) => on click of restaurant details are shown """
        pass