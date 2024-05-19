import unittest
from flask_testing import TestCase
from csit314.app import db, create_app

class BuyerLogoutTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        with self.client as client:
            # set to logged in
            client.post('/login/', json={'userid': 'user2', 'password': 'testpassword'})

    def test_logout_success(self):
        """
        <Test Data>
        userid: user2
        password: testpassword
        role: buyer
        """
        with self.client as client:
            response = client.get('/logout/')
            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertTrue(data['success'])
            self.assertEqual(data['message'], 'Logout successful')

            with client.session_transaction() as sess:
                self.assertNotIn('user_id', sess)

if __name__ == '__main__':
    unittest.main()