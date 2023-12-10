from django.test import TestCase, RequestFactory
from .views import *
from . import SCOPES
from django.utils import timezone
from datetime import timedelta
import yaml
# Create your tests here.


class NoRealUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # ========================================= get_auth_url =========================================

    def test_is_get_auth_url_post_fail(self):
        request = self.factory.post('is_authenticated')
        response = AuthURL.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_is_get_auth_url_put_fail(self):
        request = self.factory.put('is_authenticated')
        response = AuthURL.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_is_get_auth_url_delete_fail(self):
        request = self.factory.delete('is_authenticated')
        response = AuthURL.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_get_auth_url_link(self):
        request = self.factory.get('get_auth_url')
        response = AuthURL.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('https://accounts.spotify.com/authorize', response.data['url'])

    def test_get_auth_url_scopes(self):
        request = self.factory.get('get_auth_url')
        response = AuthURL.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(SCOPES.replace(' ', '+'), response.data['url'])

    # ======================================= is_authenticated =======================================

    def test_is_authenticated_post_fail(self):
        request = self.factory.post('is_authenticated')
        response = IsAuthenticated.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_is_authenticated_put_fail(self):
        request = self.factory.put('is_authenticated')
        response = IsAuthenticated.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_is_authenticated_delete_fail(self):
        request = self.factory.delete('is_authenticated')
        response = IsAuthenticated.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_is_authenticated_false(self):
        request = self.factory.get('is_authenticated')
        response = IsAuthenticated.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_authenticated'], False)

    def test_is_authenticated_false_expired_token(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() - timedelta(seconds=600),
            token_type='type'
        ).save()
        request = self.factory.get('is_authenticated')
        response = IsAuthenticated.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_authenticated'], False)

    def test_is_authenticated_error_too_many_tokens_in_db(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()
        SpotifyToken(
            user='3245678',
            refresh_token='342152637',
            access_token='32145246h',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()
        request = self.factory.get('is_authenticated')
        response = IsAuthenticated.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Too many spotify tokens saved in database', response.data['message'])

    def test_is_authenticated_true(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()
        request = self.factory.get('is_authenticated')
        response = IsAuthenticated.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_authenticated'], True)

    # ========================================= access_token =========================================

    def test_access_token_post_fail(self):
        request = self.factory.post('access_token')
        response = AccessToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_access_token_put_fail(self):
        request = self.factory.put('access_token')
        response = AccessToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_access_token_delete_fail(self):
        request = self.factory.delete('access_token')
        response = AccessToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_access_token_not_authenticated(self):
        request = self.factory.get('access_token')
        response = AccessToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_access_token_success(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()
        request = self.factory.get('access_token')
        response = AccessToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['access_token'])

    # ======================================== token_refresh =========================================

    def test_token_refresh_post_fail(self):
        request = self.factory.post('token_refresh')
        response = RefreshToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_token_refresh_put_fail(self):
        request = self.factory.put('token_refresh')
        response = RefreshToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_token_refresh_delete_fail(self):
        request = self.factory.delete('token_refresh')
        response = RefreshToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_token_refresh_not_logged_in(self):
        request = self.factory.get('token_refresh')
        response = RefreshToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not logged in', response.data['message'])

    def test_token_refresh_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()
        request = self.factory.get('token_refresh')
        response = RefreshToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ============================================ logout ============================================

    def test_logout_get_fail(self):
        request = self.factory.get('logout')
        response = Logout.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_logout_post_fail(self):
        request = self.factory.post('logout')
        response = Logout.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_logout_put_fail(self):
        request = self.factory.put('logout')
        response = Logout.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_logout_user_not_logged_in(self):
        request = self.factory.delete('logout')
        response = Logout.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User not logged in', response.data['message'])

    def test_logout_user_logged_in(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()
        request = self.factory.delete('logout')
        response = Logout.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully logged out of Spotify', response.data['message'])
        self.assertIn('https://www.spotify.com/fr/logout', response.data['url'])

    # ========================================== check_auth ==========================================

    def test_check_auth_post_fail(self):
        request = self.factory.post('check_auth')
        response = UserInfo.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_check_auth_put_fail(self):
        request = self.factory.put('check_auth')
        response = UserInfo.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_check_auth_delete_fail(self):
        request = self.factory.delete('check_auth')
        response = UserInfo.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_check_auth_not_authenticated(self):
        request = self.factory.get('check_auth')
        response = UserInfo.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_check_auth_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()
        request = self.factory.get('check_auth')
        response = UserInfo.as_view()(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ============================= create_playlist_based_on_parameters ==============================

    def test_create_playlist_based_on_parameters_get_fail(self):
        request = self.factory.get('create_playlist_based_on_parameters')
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_create_playlist_based_on_parameters_put_fail(self):
        request = self.factory.put('create_playlist_based_on_parameters')
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_create_playlist_based_on_parameters_delete_fail(self):
        request = self.factory.delete('create_playlist_based_on_parameters')
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_create_playlist_based_on_parameters_invalid_request_no_data(self):
        request_data = {}
        request = self.factory.post('create_playlist_based_on_parameters', request_data)
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_create_playlist_based_on_parameters_invalid_request_invalid_data(self):
        request_data = {'emotion': 'sadness',
                        'personalization': 'medium',
                        'popularity': 'medium',
                        'genres': ['pop', 'jazz']}
        request = self.factory.post('create_playlist_based_on_parameters', request_data)
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_create_playlist_based_on_parameters_not_authenticated(self):
        request_data = {'emotion': 'sad',
                        'personalization': 'medium',
                        'popularity': 'medium',
                        'genres': ['pop', 'jazz']}
        request = self.factory.post('create_playlist_based_on_parameters', request_data)
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_create_playlist_based_on_parameters_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request_data = {'emotion': 'sad',
                        'personalization': 'medium',
                        'popularity': 'medium',
                        'genres': ['pop', 'jazz']}
        request = self.factory.post('create_playlist_based_on_parameters', request_data)
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ======================================== save_playlist =========================================

    def test_save_playlist_get_fail(self):
        request = self.factory.get('save_playlist')
        response = SavePlaylistView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_save_playlist_put_fail(self):
        request = self.factory.put('save_playlist')
        response = SavePlaylistView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_save_playlist_delete_fail(self):
        request = self.factory.delete('save_playlist')
        response = SavePlaylistView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_save_playlist_invalid_request_no_data(self):
        request_data = {}
        request = self.factory.post('save_playlist', request_data)
        response = SavePlaylistView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_save_playlist_invalid_request_invalid_data(self):
        request_data = {'nme': 'playlist'}
        request = self.factory.post('save_playlist', request_data)
        response = SavePlaylistView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_save_playlist_not_authenticated(self):
        request_data = {'name': 'playlist'}
        request = self.factory.post('save_playlist', request_data)
        response = SavePlaylistView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_save_playlist_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request_data = {'name': 'playlist'}
        request = self.factory.post('save_playlist', request_data)
        response = SavePlaylistView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ==================================== currently_playing_song ====================================

    def test_currently_playing_song_post_fail(self):
        request = self.factory.post('currently_playing_song')
        response = CurrentlyPlayingSongView.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_currently_playing_song_put_fail(self):
        request = self.factory.put('currently_playing_song')
        response = CurrentlyPlayingSongView.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_currently_playing_song_delete_fail(self):
        request = self.factory.delete('currently_playing_song')
        response = CurrentlyPlayingSongView.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_currently_playing_song_not_authenticated(self):
        request = self.factory.get('currently_playing_song')
        response = CurrentlyPlayingSongView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_currently_playing_song_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request = self.factory.get('currently_playing_song')
        response = CurrentlyPlayingSongView.as_view()(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ========================================= player_queue =========================================

    def test_player_queue_get_fail(self):
        request = self.factory.get('player_queue')
        response = PlayerQueueView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_queue_put_fail(self):
        request = self.factory.put('player_queue')
        response = PlayerQueueView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_queue_delete_fail(self):
        request = self.factory.delete('player_queue')
        response = PlayerQueueView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_queue_invalid_request_no_data(self):
        request_data = {}
        request = self.factory.post('player_queue', request_data)
        response = PlayerQueueView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_queue_invalid_request_invalid_data(self):
        request_data = {'device_id': '324566576'}
        request = self.factory.post('player_queue', request_data)
        response = PlayerQueueView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_queue_not_authenticated(self):
        request_data = {'device_id': '324566576',
                        'song_uris': ['song_uri1', 'song_uri2']}
        request = self.factory.post('player_queue', request_data)
        response = PlayerQueueView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_player_queue_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request_data = {'device_id': '324566576',
                        'song_uris': ['song_uri1', 'song_uri2']}
        request = self.factory.post('player_queue', request_data)
        response = PlayerQueueView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ========================================= player_next ==========================================

    def test_player_next_get_fail(self):
        request = self.factory.get('player_next')
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_next_put_fail(self):
        request = self.factory.put('player_next')
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_next_delete_fail(self):
        request = self.factory.delete('player_next')
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_next_invalid_request_no_data(self):
        request_data = {}
        request = self.factory.post('player_next', request_data)
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_next_invalid_request_invalid_data(self):
        request_data = {'deviceid': '324566576'}
        request = self.factory.post('player_next', request_data)
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_next_not_authenticated(self):
        request_data = {'device_id': '324566576'}
        request = self.factory.post('player_next', request_data)
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_player_next_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request_data = {'device_id': '324566576'}
        request = self.factory.post('player_next', request_data)
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ========================================= player_pause =========================================

    def test_player_pause_get_fail(self):
        request = self.factory.get('player_pause')
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_pause_post_fail(self):
        request = self.factory.post('player_pause')
        response = PlayerPauseView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_pause_delete_fail(self):
        request = self.factory.delete('player_pause')
        response = PlayerPauseView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_pause_invalid_request_no_data(self):
        request_data = {}
        request = self.factory.put('player_pause', data=request_data, content_type='application/json')
        response = PlayerPauseView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_pause_invalid_request_invalid_data(self):
        request_data = {'deviceid': '324566576'}
        request = self.factory.put('player_pause', data=request_data, content_type='application/json')
        response = PlayerPauseView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_pause_not_authenticated(self):
        request_data = {'device_id': '324566576'}
        request = self.factory.put('player_pause', data=request_data, content_type='application/json')
        response = PlayerPauseView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_player_pause_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request_data = {'device_id': '324566576'}
        request = self.factory.put('player_pause', data=request_data, content_type='application/json')
        response = PlayerPauseView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ========================================= player_play ==========================================

    def test_player_play_get_fail(self):
        request = self.factory.get('player_play')
        response = PlayerPlayView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_play_post_fail(self):
        request = self.factory.post('player_play')
        response = PlayerPlayView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_play_delete_fail(self):
        request = self.factory.delete('player_play')
        response = PlayerPlayView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_play_invalid_request_no_data(self):
        request_data = {}
        request = self.factory.put('player_play', data=request_data, content_type='application/json')
        response = PlayerPlayView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_play_invalid_request_invalid_data(self):
        request_data = {'deviceid': '324566576'}
        request = self.factory.put('player_play', data=request_data, content_type='application/json')
        response = PlayerPlayView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_play_not_authenticated(self):
        request_data = {'device_id': '324566576'}
        request = self.factory.put('player_play', data=request_data, content_type='application/json')
        response = PlayerPlayView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_player_play_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request_data = {'device_id': '324566576'}
        request = self.factory.put('player_play', data=request_data, content_type='application/json')
        response = PlayerPlayView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # =================================== player_transfer_playback ===================================

    def test_player_transfer_playback_get_fail(self):
        request = self.factory.get('player_transfer_playback')
        response = PlayerTransferPlaybackView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_transfer_playback_post_fail(self):
        request = self.factory.post('player_transfer_playback')
        response = PlayerTransferPlaybackView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_transfer_playback_delete_fail(self):
        request = self.factory.delete('player_transfer_playback')
        response = PlayerTransferPlaybackView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_transfer_playback_invalid_request_no_data(self):
        request_data = {}
        request = self.factory.put('player_transfer_playback', data=request_data, content_type='application/json')
        response = PlayerTransferPlaybackView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_transfer_playback_invalid_request_invalid_data(self):
        request_data = {'deviceid': '324566576'}
        request = self.factory.put('player_transfer_playback', data=request_data, content_type='application/json')
        response = PlayerTransferPlaybackView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_transfer_playback_not_authenticated(self):
        request_data = {'device_id': '324566576'}
        request = self.factory.put('player_transfer_playback', data=request_data, content_type='application/json')
        response = PlayerTransferPlaybackView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_player_transfer_playback_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request_data = {'device_id': '324566576'}
        request = self.factory.put('player_transfer_playback', data=request_data, content_type='application/json')
        response = PlayerTransferPlaybackView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])

    # ====================================== player_set_volume =======================================

    def test_player_set_volume_get_fail(self):
        request = self.factory.get('player_set_volume')
        response = PlayerSetVolumeView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_set_volume_post_fail(self):
        request = self.factory.post('player_set_volume')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_set_volume_delete_fail(self):
        request = self.factory.delete('player_set_volume')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('method_not_allowed', str(response.data))

    def test_player_set_volume_invalid_request_no_data(self):
        request_data = {}
        request = self.factory.put('player_set_volume', data=request_data, content_type='application/json')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_set_volume_invalid_request_invalid_data_field(self):
        request_data = {'volumepercent': 22}
        request = self.factory.put('player_set_volume', data=request_data, content_type='application/json')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_set_volume_invalid_request_invalid_data_value_string(self):
        request_data = {'volume_percent': "sfgytdd"}
        request = self.factory.put('player_set_volume', data=request_data, content_type='application/json')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_set_volume_invalid_request_invalid_data_value_negative_number(self):
        request_data = {'volume_percent': -30}
        request = self.factory.put('player_set_volume', data=request_data, content_type='application/json')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_set_volume_invalid_request_invalid_data_value_number_bigger_than_100(self):
        request_data = {'volume_percent': 160}
        request = self.factory.put('player_set_volume', data=request_data, content_type='application/json')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_player_set_volume_not_authenticated(self):
        request_data = {'volume_percent': 22}
        request = self.factory.put('player_set_volume', data=request_data, content_type='application/json')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn('User not authenticated', response.data['message'])

    def test_player_set_volume_error(self):
        SpotifyToken(
            user='123423546',
            refresh_token='21344',
            access_token='123424r3t43',
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='type'
        ).save()

        request_data = {'volume_percent': 22}
        request = self.factory.put('player_set_volume', data=request_data, content_type='application/json')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.data['message'])


class SpotifyUserLoggedInTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        with open("spotify/test_data.yml", 'r') as file:
            self.test_data = yaml.safe_load(file)

        self.device_id = self.test_data['device_id']
        self.spotify_token = SpotifyToken(
            user='123423546',
            refresh_token=self.test_data['refresh_token'],
            access_token=self.test_data['access_token'],
            expires_in=timezone.now() + timedelta(seconds=3600),
            token_type='token_type'
        )
        self.spotify_token.save()

    # ======================================= is_authenticated =======================================
    def test_is_authenticated_true(self):
        request = self.factory.get('is_authenticated')
        response = IsAuthenticated.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_authenticated'], True)

    # ========================================= access_token =========================================

    def test_access_token_success(self):
        request = self.factory.get('access_token')
        response = AccessToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['access_token'], self.test_data['access_token'])
        self.assertEqual(response.data['refresh_token'], self.test_data['refresh_token'])

    # ======================================== token_refresh =========================================

    def test_token_refresh_success(self):
        request = self.factory.get('token_refresh')
        response = RefreshToken.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token successfully refreshed', response.data['message'])

    # ========================================== check_auth ==========================================

    def test_check_auth_success(self):
        request = self.factory.get('check_auth')
        response = UserInfo.as_view()(request)
        self.assertEqual(response.status_code, 200)

    # ============================= create_playlist_based_on_parameters ==============================

    def test_create_playlist_based_on_parameters_success(self):

        request_data = {'emotion': 'happy',
                        'personalization': 'low',
                        'popularity': 'medium',
                        'genres': ['pop', 'jazz']}
        request = self.factory.post('create_playlist_based_on_parameters', request_data)
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

    # ======================================== save_playlist =========================================

    def test_save_playlist_success(self):
        # create playlist
        request_data = {'emotion': 'happy',
                        'personalization': 'low',
                        'popularity': 'high',
                        'genres': ['pop', 'jazz']}
        request = self.factory.post('create_playlist_based_on_parameters', request_data)
        response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

        # save created playlist
        request_data = {'name': 'playlist'}
        request = self.factory.post('save_playlist', request_data)
        response = SavePlaylistView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Playlist saved successfully', response.data['message'])

    # ==================================== currently_playing_song ====================================

    def test_currently_playing_song_success(self):
        request = self.factory.get('currently_playing_song')
        response = CurrentlyPlayingSongView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    # ========================================= player_queue =========================================

    def test_player_queue_success(self):
        request_data = {'device_id': self.test_data['device_id'],
                        'song_uris': ['spotify:track:5Y4OwloGr9QSxZLZ5DXGte', 'spotify:track:24zbxPspva0ZH8hTpQ5Hm0']}
        request = self.factory.post('player_queue', data=request_data, content_type='application/json')
        response = PlayerQueueView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Songs successfully added to queue', response.data['message'])

    # ========================================= player_next ==========================================
    def test_player_next_success(self):
        request_data = {'device_id': self.test_data['device_id']}
        request = self.factory.post('player_next', request_data)
        response = PlayerNextView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Command sent', response.data['message'])

    # ========================================= player_pause =========================================

    def test_player_pause_success(self):
        request_data = {'device_id': self.test_data['device_id']}
        request = self.factory.put('player_pause', data=request_data, content_type='application/json')
        response = PlayerPauseView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Command sent', response.data['message'])

    # ========================================= player_play ==========================================

    def test_player_play_success(self):
        request_data = {'device_id': self.test_data['device_id']}
        request = self.factory.put('player_play', data=request_data, content_type='application/json')
        response = PlayerPlayView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Command sent', response.data['message'])

    # =================================== player_transfer_playback ===================================

    def test_player_transfer_playback_success(self):
        request_data = {'device_id': self.test_data['device_id']}
        request = self.factory.put('player_transfer_playback', data=request_data, content_type='application/json')
        response = PlayerTransferPlaybackView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Command sent', response.data['message'])

    # ====================================== player_set_volume =======================================

    def test_player_set_volume_success(self):
        request_data = {'volume_percent': 22}
        request = self.factory.put('player_set_volume', data=request_data, content_type='application/json')
        response = PlayerSetVolumeView.as_view({'put': 'update'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Volume set to 22%', response.data['message'])
