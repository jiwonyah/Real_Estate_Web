import unittest
from flask_testing import TestCase
from csit314.app import db, create_app
from csit314.entity.UserAccount import UserAccount
import bcrypt

class AgentLoginTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def tearDown(self):
        db.session.remove()
        #db.drop_all()

    def test_login_success(self):
        """
        <Test Data>
        userid: user4
        password: testpassword
        role: agent
        """
        with self.client as client:
            # Attempt to log in with correct credentials
            response = client.post('/login/', json={'userid': 'user4', 'password': 'testpassword'})
            self.assertEqual(response.status_code, 200)

            # Check if session variable is set after successful login
            with client.session_transaction() as sess:
                self.assertIn('user_id', sess)

    def test_login_failure_invalid_userid(self):
        with self.client as client:
            # Attempt to log in with invalid user
            response = client.post('/login/', json={'userid': 'invaliduser', 'password': 'testpassword'})
            self.assertEqual(response.status_code, 401)

    def test_login_failure_invalid_password(self):
        with self.client as client:
            # Attempt to log in with invalid password
            response = client.post('/login/', json={'userid': 'user4', 'password': 'wrongpassword'})
            self.assertEqual(response.status_code, 401)

    def test_login_failure_invalid_userid_password(self):
        with self.client as client:
            # Attempt to log in with invalid userid and password
            response = client.post('/login/', json={'userid': 'invaliduser', 'password': 'wrongpassword'})
            self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()