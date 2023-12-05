from django.test import TestCase, RequestFactory
from .views import (Logout, AuthURL, PlaylistBasedOnParametersView)

# Create your tests here.


class LogoutTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_logout_not_logged_in(self):
        request = self.factory.delete('logout', {})
        response = Logout.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User not logged in', response.data['message'])

    def test_logout(self):
        # # TODO: LOGIN ???
        # request = self.factory.get('get-auth-url', {})
        # response = AuthURL.as_view()(request)
        # auth_url = response.data['url']
        # print(auth_url)
        # request = self.factory.post(auth_url, {})
        # print(request)

        request = self.factory.delete('logout', {})
        response = Logout.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully logged out of Spotify', response.data['message'])




class PlaylistBasedOnParametersTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_invalid_request(self):
        request_data = {}
        request = self.factory.post('create_playlist_based_on_parameters', request_data)
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_valid_request(self):
        request_data = {
            'emotion': 'happy',
            'personalization': 'low',
            'popularity': 'low',
            'genres': [
                'genre1',
                'genre2',
                'genre3'
            ]
        }
        request = self.factory.post('create_playlist_based_on_parameters', request_data)
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)