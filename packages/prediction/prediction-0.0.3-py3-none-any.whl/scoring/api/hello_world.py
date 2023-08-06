"""
This module will hold api utils.
"""
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

class HelloWorldSerializer(serializers.Serializer):
    hello = serializers.CharField(required=True)
    world = serializers.CharField(required=True)


class HelloWorld(APIView):
    """
    Demo class to be used as a reference for building API Views.
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        Validate input and return a json response.
        """
        serializer = HelloWorldSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'hello': 'world'})