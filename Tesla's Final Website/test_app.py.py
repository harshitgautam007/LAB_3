import unittest
from app import app
import coverage

class TestAdminLogin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.cov = coverage.Coverage()
        self.cov.start()

    def tearDown(self):
        self.cov.stop()
        self.cov.save()

    # Test if login is successful
    def test_admin_login_success(self):
        response = self.app.post('/admin_login', data=dict(
            organization_id='org123',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to your organization', response.data)
        self.assertIn(b'Logout', response.data)

    # Test if incorrect password results in failure
    def test_admin_login_incorrect_password(self):
        response = self.app.post('/admin_login', data=dict(
            organization_id='org123',
            password='wrong_password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'incorrect password', response.data)
        self.assertNotIn(b'No such organization exists', response.data)
        self.assertNotIn(b'Required fields have not been filled', response.data)

    # Test if invalid organization ID results in failure
    def test_admin_login_invalid_org_id(self):
        response = self.app.post('/admin_login', data=dict(
            organization_id='invalid_org_id',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No such organization exists', response.data)
        self.assertNotIn(b'incorrect password', response.data)
        self.assertNotIn(b'Required fields have not been filled', response.data)

    # Test if required fields have not been filled
    def test_admin_login_missing_fields(self):
        response = self.app.post('/admin_login', data=dict(
            organization_id='',
            password=''
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Required fields have not been filled', response.data)
        self.assertNotIn(b'No such organization exists', response.data)
        self.assertNotIn(b'incorrect password', response.data)

if __name__ == '_main_':
    unittest.main()