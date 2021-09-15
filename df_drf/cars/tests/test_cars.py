import json

from django.contrib.auth.models import User
from cars.models import Brand, Car
from oauth2_provider.models import Application
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

class CarTestCase(TestCase):

    def setUp(self):
        user = User(username='api_test')
        user.set_password('cyPNjhx9aNADjF4Z')
        user.save()
        application = Application.objects.create(user=user, authorization_grant_type='password', client_type='confidential', name='api_test')
        Brand.objects.create(name='Test Brand 1', created='2019-01-01T01:00:00Z')
        Brand.objects.create(name='Test Brand 2', created='2019-01-01T01:00:00Z')

        client = APIClient()

        data = {'grant_type': application.authorization_grant_type, 'username': user.username, 'password': 'cyPNjhx9aNADjF4Z', 'client_id': application.client_id, 'client_secret':  application.client_secret}

        response = client.post('/oauth2/access_token/', data)

        result = json.loads(response.content)
        self.access_token = result['access_token']
        self.user = user

    def test_create_car(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_car = {'name': 'Test', 'height': '1.19', 'width': '1.76', 'brand': Brand.objects.first().name}

        response = client.post('/carmodels/', test_car, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('height', result)
        self.assertIn('name', result)
        self.assertIn('width', result)
        self.assertIn('brand', result)

        car = None
        if 'id' in result:
            del result['id']

        self.assertEqual(result, test_car)

    def test_update_car(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        car = Car.objects.create(name='Test Update', height=1, width=1, brand=Brand.objects.first())

        test_car_update = {'name': 'New Test Update', 'height': '2.00', 'width': '3.00', 'brand': Brand.objects.last().name}

        response = client.put(f'/carmodels/{car.id}/', test_car_update, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'id' in result:
            del result['id']

        self.assertEqual(result, test_car_update)

    def test_delete_car(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        car = Car.objects.create(name='Test Delete', height='1.00', width='1.00', brand=Brand.objects.first())

        response = client.delete(f'/carmodels/{car.id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        car_exists = Car.objects.filter(id=car.id)
        self.assertFalse(car_exists)

    def test_get_car(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        test_car = {'name': 'New Test Update', 'height': '2.00', 'width': '3.00', 'brand': Brand.objects.last().name}
        car = Car.objects.create(name=test_car['name'], height=test_car['height'], width=test_car['width'], brand=Brand.objects.get(name=test_car['brand']))

        response = client.get(f'/carmodels/{car.id}/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'id' in result:
            del result['id']

        self.assertEqual(result, test_car)

    def test_list_cars(self):

        client = APIClient()
        client.force_authenticate(user=self.user, token=self.access_token)

        Car.objects.create(name='Test Car List 1', height='1.00', width='1.00', brand=Brand.objects.first())
        Car.objects.create(name='Test Car List 2', height='3.45', width='2.65', brand=Brand.objects.first())

        response = client.get('/carmodels/')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(result), 2)

        for car in result:
            self.assertIn('id', car)
            self.assertIn('height', car)
            self.assertIn('name', car)
            self.assertIn('width', car)
            self.assertIn('brand', car)
