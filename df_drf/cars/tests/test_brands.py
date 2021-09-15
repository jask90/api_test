import json

from django.contrib.auth.models import User
from cars.models import Brand, Car
from oauth2_provider.models import Application
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

class BrandTestCase(TestCase):

    def setUp(self):
        user = User(username='api_test')
        user.set_password('cyPNjhx9aNADjF4Z')
        user.save()
        application = Application.objects.create(user=user, authorization_grant_type='password', client_type='confidential', name='api_test')

        client = APIClient()

        data = {'grant_type': application.authorization_grant_type, 'username': user.username, 'password': 'cyPNjhx9aNADjF4Z', 'client_id': application.client_id, 'client_secret':  application.client_secret}

        response = client.post('/oauth2/access_token/', data)

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user

    def test_create_brand(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_brand = {'name': 'Test', 'created': '1947-01-01T00:00:00Z',}

        response = client.post('/carbrands/', test_brand, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('created', result)
        self.assertIn('name', result)
        self.assertIn('created_at', result)
        self.assertIn('num_of_cars', result)

        brand = None
        if 'id' in result:
            del result['id']
        if 'num_of_cars' in result:
            del result['num_of_cars']
        if 'created_at' in result:
            del result['created_at']

        self.assertEqual(result, test_brand)

    def test_update_brand(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        brand = Brand.objects.create(name='Test Update',created='2021-01-01T00:00:00Z',)

        test_brand_update = {'name': 'New Test Update','created': '2021-01-01T00:00:00Z',}

        response = client.put(f'/carbrands/{brand.id}/', test_brand_update, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'id' in result:
            del result['id']
        if 'created_at' in result:
            del result['created_at']
        
        test_brand_update['num_of_cars'] = brand.num_of_cars

        self.assertEqual(result, test_brand_update)

    def test_delete_brand(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        brand = Brand.objects.create(name='Test Delete',created='2020-01-01T00:00:00Z',)

        response = client.delete(f'/carbrands/{brand.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        brand_exists = Brand.objects.filter(id=brand.id)
        self.assertFalse(brand_exists)

    def test_delete_brand_with_cars(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        brand = Brand.objects.create(name='Test Delete With Cars',created='2020-01-01T00:00:00Z',)
        car = Car.objects.create(name='Car Test', height=1, width=1, brand=brand)

        response = client.delete(f'/carbrands/{brand.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        brand_exists = Brand.objects.filter(id=brand.id)
        self.assertTrue(brand_exists)

    def test_get_brand(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_brand = {'name': 'Test Get', 'created': '2019-01-01T00:00:00Z'}
        brand = Brand.objects.create(name=test_brand['name'], created=test_brand['created'])

        response = client.get(f'/carbrands/{brand.id}/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'id' in result:
            del result['id']
        if 'created_at' in result:
            del result['created_at']
        
        test_brand['num_of_cars'] = brand.num_of_cars
        self.assertEqual(result, test_brand)

    def test_list_brands(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        Brand.objects.create(name='Test Brand List 1', created='2019-01-01T01:00:00Z')
        Brand.objects.create(name='Test Brand List 2', created='2019-01-01T02:00:00Z')

        response = client.get('/carbrands/')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(result), 2)

        for brand in result:
            self.assertIn('id', brand)
            self.assertIn('created', brand)
            self.assertIn('name', brand)
            self.assertIn('created_at', brand)
            self.assertIn('num_of_cars', brand)
