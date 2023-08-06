"""
This module will hold our hello world api test
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HelloWorldTest(APITestCase):

    def setUp(self):
        self.base_uri = reverse('hello-world')

    def test_get_hello_world_without_required_params(self):
        """
        Should return a 400 Bad request.
        """
        resp = self.client.get(path=self.base_uri)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_hello_world(self):
        """
        Should return a json response with 200 OK.
        """
        query_params = {'hello': 'hello', 'world': 'world'}
        resp = self.client.get(path=self.base_uri, data=query_params)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['hello'], 'world')