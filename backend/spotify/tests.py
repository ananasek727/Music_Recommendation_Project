from django.test import TestCase, RequestFactory
from .views import (Logout)

# Create your tests here.


class LogoutTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_invalid_request(self):
        request = self.factory.delete('logout', {})
        response = Logout.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully logged out of Spotify', response.data['message'])

