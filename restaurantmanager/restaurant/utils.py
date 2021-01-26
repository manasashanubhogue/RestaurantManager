import functools
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from django.core.cache import cache
from restaurantmanager.restaurant.models import Menu, MenuItemType, Restaurant, PermissionTypeEnum

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
    elif Restaurant.get_restaurant_data({Q(manager_id=user.id)}).exists():
        filter_param = Q(manager_id=user.id)
    else:
        return False, None
    return True, filter_param

def is_restaurant_manager(user, restaurant_id):
    """ True if user is the manager of the given restaurant """
    return Restaurant.get_restaurant_data({Q(id=restaurant_id, manager_id=user.id)}).exists()

def has_permission_to_edit_restaurant(user, restaurant_id):
    """ SuperUser is allowed to edit any restaurant
    Manager can edit only thier restaurants """
    if user.is_superuser:
        return True
    elif is_restaurant_manager(user, restaurant_id):
        return True
    else:
        return False

#TODO - FUTURE USAGE? - FE to know which buttons/actions to allow
def get_permission_list(user):
    # gets allowed actions for user
    permission_list = []
    if has_permission_to_manage_restaurant(user):
        permission_list.append(PermissionTypeEnum.CAN_MANAGE_RESTAURANT)
    return permission_list

def get_menu_and_item_type():
    """ Fetch meta data required and cache it for other api usage """
    menu_item_type = cache.get('menu_item_type_cached', None)
    if (menu_item_type is None):
        menu_item_type = MenuItemType.get_menu_item_types()
        cache.set('menu_item_type_cached', menu_item_type)

    menu = cache.get('menu_cached', None)
    if (menu is None):
        menu = Menu.get_menu()
        cache.set('menu_cached', menu)
    return menu_item_type, menu
