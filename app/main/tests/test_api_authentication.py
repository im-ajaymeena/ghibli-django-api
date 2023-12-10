from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings
from main.models import Film
import uuid

class FilmListAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('film-list')
        self.valid_secret_key = settings.GHIBLIKEY
        self.invalid_secret_key = 'invalid_key'

        # Create some test films
        self.film1 = Film.objects.create(
            id=uuid.uuid4(),
            title='Film 1',
            original_title='Original Title 1',
            release_date='2023',
            director='Director 1'
        )
        self.film2 = Film.objects.create(
            id=uuid.uuid4(),
            title='Film 2',
            original_title='Original Title 2',
            release_date='2023',
            director='Director 2'
        )

    def test_valid_secret_key(self):
        # Set the valid secret key
        self.client.defaults['HTTP_X_SECRET_KEY'] = self.valid_secret_key

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming there are 2 films in the database

    def test_invalid_secret_key(self):
        # Set an invalid secret key
        self.client.defaults['HTTP_X_SECRET_KEY'] = self.invalid_secret_key

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "Access Denied - Unauthorized"})

    def test_missing_secret_key(self):
        # Do not set a secret key header
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "Access Denied - Unauthorized"})
