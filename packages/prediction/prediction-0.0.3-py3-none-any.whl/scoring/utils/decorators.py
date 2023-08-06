"""
This module will hold our reusable decorators.
"""
from functools import wraps
from rest_framework import status
from rest_framework.response import Response


def serializer_class(serializer_class):
    """
    Decorator to wrap DRF api methods to enable data validation using a serializer class.

    Args:
        serializer_class (RestFramework Serializer) : the serializer class to use for the validation.

    Returns:
         a 400 bad request if validation fails, else call the api method.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            # Check the request method, and get the data accordingly
            if request.method == 'GET':
                serializer_data = request.query_params
            else:
                serializer_data = request.data
            serializer_instance = serializer_class(data=serializer_data)
            # If serializer is valid, call the decorated func, else return bad request
            if not serializer_instance.is_valid():
                return Response(serializer_instance.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return func(request)
        return wrapper
    return decorator