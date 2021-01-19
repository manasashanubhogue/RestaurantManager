import re
from django.shortcuts import render
from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from restaurantmanager.restaurant.models import Restaurant, User
from restaurantmanager.restaurant.utils import validate_params

class UserDetailsAPI(viewsets.ViewSet):
     
    #TODO: handle validation of email/ph, loggers
    @validate_params({'email': str, 'first_name': str, 'last_name': str, 'password': str})
    def create_user(self, request):
        """ Function to create user for the application """
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

class RestaurantDetailsAPI(viewsets.ViewSet):

    def restaurant_meta_data(self, request):
        # user = request.user
        restaurants = Restaurant.get_restaurant_data({}, values=['id', 'name'])
        return Response(restaurants)

    # @validate_params({'restaurant_id': int})
    def get_restaurant_data(self, request, restaurant_id):
        """ Based on id passed get detais"""
        import pdb;pdb.set_trace()
        # user = request.user
        restaurants = Restaurant.get_restaurant_data({Q(id=restaurant_id)})
        return Response(restaurants)

    def add_restaurant_details(self, request):
        """ Add new restaurant """
        # anyone who is authenticated can add restaurant
        pass

    def edit_restaurant_details(self, request):
        # has permission - restaurant id valid, must be manager of that res or admin
        # if publishes - send it for verification
        pass
 
