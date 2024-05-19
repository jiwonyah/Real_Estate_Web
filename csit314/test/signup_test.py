import unittest
from flask_testing import TestCase
from csit314.app import db, create_app
from csit314.entity.UserAccount import User, Role
from flask import json

class TestSignUpController(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    def test_signup_success(self):
        form_data = {
            'userid': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test@example.com',
            'role': Role.BUYER.value  # Choose any role you want to test without ADMIN
        }

        # Create a POST request with form data
        with self.client as client:
            response = client.post('/signup/', data=form_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Parse JSON response
            response_data = json.loads(response.data)

            # Check if user was created successfully
            self.assertTrue(response_data['success'])
            self.assertEqual(response_data['message'], 'User created successfully')

            # Retrieve the created user from the database
            user = User.query.filter_by(userid=form_data['userid']).first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, form_data['email'])
            self.assertEqual(user.role.value, form_data['role'])

    def test_signup_failure(self):
        """
        Attempt to create a user with existing userid
        After attempting to sign up for membership with an already registered userid,
        check by email whether the user has actually been created.
        """
        existing_user = User(userid='existinguser', password='existingpassword', email='existing@example.com',
                             firstName='Test', lastName='User', role=Role.SELLER.value)
        db.session.add(existing_user)
        db.session.commit()

        form_data = {
            'userid': 'existinguser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'newuser@example.com',
            'role': Role.AGENT.value
        }
        # Create a POST request with form data --> signup must be failed
        response = self.client.post('/signup/', data=form_data, follow_redirects=True)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])  # Check if 'success' is False indicating failure
        self.assertTrue('error' in response_data)  # Check if 'error' message is present in response

        # Check if user creation failed using email(unique) --> the user must not be found
        user = User.query.filter_by(email=form_data['email']).first()
        self.assertIsNone(user) # it must be True

    def test_signup_failure2(self):
        """
        Attempt to create a user with admin role
        Since ADMIN user cannot be created by sign up function but can be created by the system,
        it must be rejected if sign up registration with admin role is submitted.
        """
        form_data = {
            'userid': 'testuser2',
            'password': 'testpassword',
            'password2': 'testpassword',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test2@example.com',
            'role': Role.ADMIN.value
        }

        # Create a POST request with form data --> signup must be failed
        response = self.client.post('/signup/', data=form_data, follow_redirects=True)
        response_data = response.get_json()
        self.assertFalse(response_data['success'])  # Check if 'success' is False indicating failure
        self.assertTrue('error' in response_data)  # Check if 'error' message is present in response

        # Check if user creation failed --> the user must not be found
        user = User.query.filter_by(userid=form_data['userid']).first()
        self.assertIsNone(user) # it must be true

if __name__ == '__main__':
    unittest.main()
