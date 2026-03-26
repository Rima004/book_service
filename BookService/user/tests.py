from http.client import responses

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status, response

User = get_user_model()

class UserTestViews(APITestCase):

    fixtures = ["users.json"]

    def setUp(self):

        self.client_user = User.objects.get(pk=1)
        self.provider_user = User.objects.get(pk=2)
        self.data_for_client = {
            "first_name": "kiki",
            "last_name": "second",
            "email": "clients@mail.com",
            "username": "liki",
            "password": "clientmy123",
            "phone_number": "+37368205306",
            "role": "client",
        }
        self.data_for_provider = {
            "first_name": "stepan",
            "last_name": "popovici",
            "email": "providers@mail.com",
            "username": "pr",
            "password": "provider123",
            "phone_number": "+37368254306",
            "role": "provider",

        }

    def test_get_unauthenticated_user(self):
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_authenticated_user(self):
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_client(self):
        response = self.client.post("/api/user/",self.data_for_client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.data_for_client["email"]).exists())

    def test_user_cannot_update_other_user(self):
        self.client.force_authenticate(user=self.client_user)

        data = {
            "first_name": "Bob",
            "last_name": "Bobi",
        }

        response = self.client.patch(
            f"/api/user/{self.provider_user.id}/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_authenticated_client(self):
        self.client.force_authenticate(user=self.client_user)

        new_data = {
            "first_name": "John",
            "phone_number" :"+37368205356",
            "username": "piki_cici"
        }

        response = self.client.patch(f"/api/user/{self.client_user.id}/",new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_user.refresh_from_db()
        self.assertEqual(self.client_user.first_name,new_data["first_name"])
        self.assertEqual(self.client_user.phone_number, new_data["phone_number"])
        self.assertEqual(str(self.client_user.username), new_data["username"])

    def test_create_provider(self):

        response = self.client.post("/api/user/",self.data_for_provider)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.data_for_provider["email"]).exists())



    def test_update_authenticated_provider(self):
        self.client.force_authenticate(user=self.provider_user)
        new_data ={
            "first_name": "Liki",
            "phone_number": "+37368205666",
            "username": "cici"
        }
        response = self.client.patch(f"/api/user/{self.provider_user.id}/",new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.provider_user.refresh_from_db()
        self.assertEqual(self.provider_user.first_name, new_data["first_name"])
        self.assertEqual(self.provider_user.phone_number, new_data["phone_number"])
        self.assertEqual(self.provider_user.username, new_data["username"])

    def test_user_cannot_delete_self_or_other(self):

        self.client.force_authenticate(user=self.client_user)
        response_self = self.client.delete(f"/api/user/{self.client_user.id}/")
        self.assertEqual(response_self.status_code, status.HTTP_403_FORBIDDEN)

        response_other =self.client.delete(f"/api/user/{self.provider_user.id}/")
        self.assertEqual(response_other.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.provider_user)

        response_self_provider = self.client.delete(f"/api/user/{self.provider_user.id}/")
        self.assertEqual(response_self_provider.status_code, status.HTTP_403_FORBIDDEN)


        response_other_client = self.client.delete(f"/api/user/{self.client_user.id}/")
        self.assertEqual(response_other_client.status_code, status.HTTP_403_FORBIDDEN)





