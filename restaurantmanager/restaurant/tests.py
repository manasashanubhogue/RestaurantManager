import json
from django.urls import reverse
from django.test import TestCase, Client
from restaurantmanager.restaurant.models import User
from restaurantmanager.restaurant.constants import SUCCESS_MESSAGES
from rest_framework import status

class BaseTestCase(TestCase):
    """ Base Test Class, Test cases must inherit this class """
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super().__init__(*args, **kwargs)

    def create_mock_user(self, username="superuser", password="superuser", email="superuser@gmail.com", is_superuser=True):
        """ Mock User """
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.is_superuser = is_superuser
        user.save()
        self.user = user

    def create_mock_client(self, username="superuser", password="superuser"):
        """ Mock Test User """
        self.client.login(username=username, password=password)

class TestUserDataFlow(BaseTestCase):

    def setUp(self):
        """ login as superuser """
        self.create_mock_user()
        self.create_mock_client()
        # data required for testing below cases
        json_data = open('restaurantmanager/mock_data/users.json')
        self.data = json.load(json_data)

    def test_user_creation(self):
        """ Test case to verify user creation api """
        response = self.client.post(reverse('create_new_user',),
                                    data=self.data, content_type='application/json')
        self.assertEqual(response.data, SUCCESS_MESSAGES['USER_CREATED'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_data_retrival(self):
        """ Test case to verify get_users api """
        # create a new user
        self.client.post(reverse('create_new_user',),
                                    data=self.data, content_type='application/json')
        # since loggedin as super user, response should contain data of superuser and above created user
        response = self.client.get(reverse('get_app_users'))
        self.assertEqual(response.data.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestRestaurantAPIs(BaseTestCase):
    fixtures = ['users.json']

    def setUp(self):
        """ login as superuser """
        self.create_mock_user()
        self.create_mock_client()
        # data required for testing below cases
        json_data = open('restaurantmanager/mock_data/restaurants.json')
        self.data = json.load(json_data)

    def test_restaurant_creation(self):
        response = self.client.post(reverse('create_restaurant',),
                                    data=self.data, content_type='application/json')
        self.assertEqual(response.data.count(), len(self.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
