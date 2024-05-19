import unittest
from flask_testing import TestCase
from csit314.app import db, create_app
from flask import json,request, g, session
from csit314.entity.PropertyListing import FloorLevel, Furnishing, PropertyType
import logging

class TestSignUpController(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        self.login()

    def login(self):
        return self.client.post('/login/', json={'userid': 'user4', 'password': 'testpassword'})

    def test_create_property_listing_success(self):
        with self.client as client:
            response = client.post('/propertyListing/create/', data={
                'subject': 'test',
                'content': '',
                'price': 100000,
                'address': 'yuan ching road',
                'floorSize': 50,
                'floorLevel': 'low',
                'propertyType': 'hdb',
                'furnishing': 'not_furnished',
                'builtYear': 2010,
                'client_id': 'user3',
                'images': []
            })

            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertIn('Property listing created successfully', data['message'])

    def test_creating_property_fail1(self):
        with self.client as client:
            data = {
                'client_id': 'user3',
                'address': 'yuan ching road',
                'builtYear': 2010,
                'images': []
            }
            response = client.post('/propertyListing/create/', data=json.dumps(data),
                                   content_type='application/json', follow_redirects=True)

            response_data = response.get_json()
            self.assertFalse(response_data['success'])

    def test_creating_property_fail2(self):
        # input invalid user id in the client_id field
        with self.client as client:
            data = {
                'subject': 'test',
                'content': '',
                'price': 100000,
                'address': 'yuan ching road',
                'floorSize': 50,
                'floorLevel': 'low',
                'propertyType': 'hdb',
                'furnishing': 'not_furnished',
                'builtYear': 2010,
                'client_id': 'invalidUser',
                'images': []
            }
            response = client.post('/propertyListing/create/', data=json.dumps(data),
                                   content_type='application/json', follow_redirects=True)

            response_data = response.get_json()
            self.assertFalse(response_data['success'])


    def test_creating_property_fail3(self):
        # input user whose role is not 'seller' in the client_id field
        with self.client as client:
            data = {
                'subject': 'test',
                'content': '',
                'price': 100000,
                'address': 'yuan ching road',
                'floorSize': 50,
                'floorLevel': 'low',
                'propertyType': 'hdb',
                'furnishing': 'not_furnished',
                'builtYear': 2010,
                'client_id': 'user1',
                'images': []
            }
            response = client.post('/propertyListing/create/', data=json.dumps(data),
                                   content_type='application/json', follow_redirects=True)

            response_data = response.get_json()
            self.assertFalse(response_data['success'])


    # def test_creating_property_success(self):
    #     with self.client as client:
    #         data = {
    #             'client_id': 'user3',
    #             'subject': 'test',
    #             'content': '',
    #             'price': 100000,
    #             'address': 'yuan ching road',
    #             'floorSize': 50,
    #             'floorLevel': FloorLevel.LOW.value,
    #             'propertyType': PropertyType.HDB.value,
    #             'furnishing': Furnishing.NotFurnished.value,
    #             'builtYear': 2010,
    #             'images': []
    #         }
    #         response = client.post('/propertyListing/create/', data=json.dumps(data),
    #                                content_type='application/json', follow_redirects=True)
    #
    #         response_data = response.get_json()
    #         print("Response JSON:", response_data)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTrue(response_data['success'])
    #         self.assertEqual(response_data['message'], 'Property listing created successfully')

if __name__ == '__main__':
    unittest.main()
