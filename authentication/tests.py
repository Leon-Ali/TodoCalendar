from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class UserTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            'testuser', 'test@example.com', 'testpassword'
        )

        self.signup_url = reverse('signup')

    def test_create_user(self):
        """
        Ensure we can crate a new user
        """
        data = {
            'username':'johndoe',
            'email':'johndoe@test.com',
            'password':'somepassword'
        }

        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['username'], data['username'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
            'username': 'johndoe',
            'email': 'johndoe@test.com',
            'password': 'john'

        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
            'username': 'johndoe',
            'email': 'johndoe@test.com',
            'password': ''

        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'johndoe'*10,
            'email': 'johndoe@test.com',
            'password': 'johndoe222'
        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
            'username': '',
            'email': 'johndoe@test.com',
            'password': 'johndoe222'
        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
            'username': 'testuser',
            'email': 'johndoe@test.com',
            'password': 'johndoe222'
        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'johndoe',
            'email': 'test@example.com',
            'password': 'johndoe222'
        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'johndoe',
            'email': 'johndoe',
            'password': 'johndoe222'
        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            'username': 'johndoe',
            'email': '',
            'password': 'johndoe222'
        }

        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_user_can_obtain_token(self):
        token_obtain_url = reverse('token_obtain_pair')
        data = {
            'username':'testuser',
            'password':'testpassword'
        }
        response = self.client.post(token_obtain_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_can_refresh_token(self):
        token_obtain_url = reverse('token_obtain_pair')
        token_refresh_url = reverse('token_refresh')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        token_obtain = self.client.post(token_obtain_url, data, format='json')
        refresh_token = {'refresh':token_obtain.data['refresh']}
        response = self.client.post(token_refresh_url, refresh_token, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)











