import functools
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from restaurantmanager.restaurant.models import Restaurant

def validate_params(required_params={}):
    '''
        To validate parameters required - {'param': str/int, ..}
        Checks if required paramter exists along with its datatype
    '''
    def decorator_validate_params(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            request_data = request.data
            err_msg_list = set()
            for key, value in required_params.items():
                data_value = request_data.get(key, None)
                if data_value:
                    if not type(data_value) is value:
                        err_msg_list.add('Invalid data type for {}:{} should have been {}'.format(
                            key, type(data_value), value))
                else:
                    err_msg_list.add('Missing parameter :' + str(key))

            if len(err_msg_list) != 0:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"errors": err_msg_list})

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator_validate_params


def has_permission_to_manage_restaurant(user):
    """ Based  on permission level , return filters applicable """
    if user.is_superuser:
        filter_param = Q()
    elif Restaurant.objects.filter(manager_id=user.id).exists():
        filter_param = Q(manager_id=user.id)
    else:
        return False, None
    return True, filter_param

def is_restaurant_manager(user, restaurant_id):
    """ True if user is the manager of the given restaurant """
    return Restaurant.objects.filter(manager_id=user.id, id=restaurant_id).exists()

def has_permission_to_edit_restaurant(user, restaurant_id):
    """ SuperUser is allowed to edit any restaurant 
    Manager can edit only thier restaurants """
    if user.is_superuser:
        return True
    elif is_restaurant_manager(user, restaurant_id):
        return True
    else:
        return False