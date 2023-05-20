from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Admin

token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiand0X3ZlcnNpb24iOjEsImV4cCI6MTY4NTExNzEzOH0.I_ftmJ-33KkL14Dpw4HGVD-6p14pd007UwQwllc3kBQ"


class AdminAPITestCase(APITestCase):
    def setUp(self):
        Admin.objects.create(
            username="admin", password="admin", email="1@qq.com"
        ).save()

    def test_user_list(self):
        url = reverse("user_list")
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=token)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
