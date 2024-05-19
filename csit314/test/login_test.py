import unittest
from flask_testing import TestCase
from csit314.app import db, create_app
from csit314.entity.UserAccount import UserAccount

class LoginTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        # create sample test user (signup)
        form_data = {
            'userid': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test@example.com',
            'role': 'buyer' # Choose any role you want to test without ADMIN
        }

        # Create a POST request with form data
        # Add only when there are no existing user with userid 'testuser'
        existing_user = UserAccount.query.filter_by(userid='testuser').first()
        if not existing_user:
            self.client.post('/signup/', data=form_data, follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    def test_login_success(self):
        with self.client as client:
            # Attempt to log in with correct credentials
            response = client.post('/login/', json={'userid': 'testuser', 'password': 'testpassword'})
            self.assertEqual(response.status_code, 200)

            # Check if session variable is set after successful login
            with client.session_transaction() as sess:
                self.assertIn('user_id', sess)

    def test_login_failure_invalid_user(self):
        with self.client as client:
            # Attempt to log in with invalid user
            response = client.post('/login/', json={'userid': 'invaliduser', 'password': 'testpassword'})
            self.assertEqual(response.status_code, 401)

    def test_login_failure_invalid_password(self):
        with self.client as client:
            # Attempt to log in with invalid password
            response = client.post('/login/', json={'userid': 'testuser', 'password': 'wrongpassword'})
            self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
