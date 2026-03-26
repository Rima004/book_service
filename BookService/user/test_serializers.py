from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from yaml import serialize
from .serializers import *
User = get_user_model()

class UserTestSerializers(APITestCase):
    fixtures = ["users.json"]


    def setUp(self):
        self.valid_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@mail.com",
            "username": "alice123",
            "password": "StrongPass123!",
            "phone_number": "+37368205310",
            "role": "client"
        }

    def test_register_serializer_with_valid_data(self):
        serializer = UserRegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, self.valid_data["first_name"])
        self.assertEqual(user.last_name, self.valid_data["last_name"])
        self.assertEqual(user.email, self.valid_data["email"])
        self.assertEqual(user.username, self.valid_data["username"])

    def test_register_serializer_missing_required_field(self):
        data = self.valid_data.copy()
        data.pop("email")
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_register_serializer_invalid_password(self):
        data = self.valid_data.copy()
        data["password"]='123'
        serializer = UserRegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


