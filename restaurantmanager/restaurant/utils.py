import functools
from rest_framework import status
from rest_framework.response import Response


def validate_params(required_params={}):
    '''
        Decorator to validate the required params in request object.
        args : required_params format example : {'param1': str, 'param2': int}
        Validates:
            1. parameter existence
            2. Data type match for respective parameter
        returns : 400 BAD request if any above condition fails with list of errors.
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