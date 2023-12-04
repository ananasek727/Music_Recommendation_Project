from django.shortcuts import render, redirect
from .util import update_or_create_user_tokens, is_spotify_authenticated, execute_spotify_api_request, \
    delete_user_tokens
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework.response import Response
from rest_framework import status
from .models import SpotifyToken


class AuthURL(APIView):
    def get(self, request, format=None):
        # TODO: ???? scopes? client_id?
        scopes = 'streaming user-read-email user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing'
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    ).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token
    )

    # TODO: url to main site
    return redirect('is_authenticated')
    # return redirect('http://localhost:3000/')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated, access_token = is_spotify_authenticated(
            self.request.session.session_key
        )
        return Response({'authentication_status': is_authenticated,
                         'access_token': access_token}, status=status.HTTP_200_OK)


class Logout(APIView):
    def delete(self, request, format=None):
        user_tokens = SpotifyToken.objects.all()
        if len(user_tokens) == 0:
            Response({'message': 'User not logged in.'}, status=status.HTTP_200_OK)
        print(f"user tokens 0 {user_tokens}")

        try:
            delete_user_tokens()
        except Exception as e:
            return Response({'message': f'Error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print(f"user tokens 1 {user_tokens}")
        return Response({'message': 'Successfully logged out of Spotify.',
                         'url': 'https://www.spotify.com/fr/logout'}, status=status.HTTP_200_OK)


class CheckAuth(APIView):
    def get(self, request, format=None):
        if not SpotifyToken.objects.exists():
            return Response({'message': 'not authenticated'}, status=status.HTTP_200_OK)
        token = SpotifyToken.objects.last()
        print("-=--")
        print(token.access_token)
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(token, endpoint)
        print(response)
        if 'Error' in response:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response, status=status.HTTP_200_OK)


def get_playlist():
    dawid_id = '6EB8VE9f7Ut6NOgviN6gDW'

    if not SpotifyToken.objects.exists():
        return Response({'message': 'Unauthorized user.'}, status=status.HTTP_401_UNAUTHORIZED)

    token = SpotifyToken.objects.last()
    endpoint = "recommendations"
    request_data = {}
    response = execute_spotify_api_request(token, endpoint, request_data)
    print(response)
    # if 'error' in response or 'item' not in response:
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)
    #
    # item = response.get('item')
    # duration = item.get('duration_ms')
    # progress = response.get('progress_ms')
    # album_cover = item.get('album').get('images')[0].get('url')
    # is_playing = response.get('is_playing')
    # song_id = item.get('id')
    #
    # artist_string = ""
    #
    # for i, artist in enumerate(item.get('artists')):
    #     if i > 0:
    #         artist_string += ", "
    #     name = artist.get('name')
    #     artist_string += name
    #
    # song = {
    #     'title': item.get('name'),
    #     'artist': artist_string,
    #     'duration': duration,
    #     'time': progress,
    #     'image_url': album_cover,
    #     'is_playing': is_playing,
    #     'votes': 0,
    #     'id': song_id
    # }
    #
    # return Response(song, status=status.HTTP_200_OK)


class UserInfo(APIView):
    def get(self, request, format=None):
        if not SpotifyToken.objects.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        token = SpotifyToken.objects.last()
        print(token.access_token)
        endpoint = ""
        response = execute_spotify_api_request(token, endpoint)
        print(response)

        return Response(response, status=status.HTTP_200_OK)
