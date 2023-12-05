from django.shortcuts import render, redirect
from .util import (update_or_create_user_tokens, is_spotify_authenticated, execute_spotify_api_request,
                   delete_user_tokens, get_user_tokens, get_users_top_artists, get_users_top_tracks,
                   get_recommendations, delete_songs, save_playlist, get_currently_playing_song)
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework.response import Response
from rest_framework import status
from .models import SpotifyToken, Song
from rest_framework import viewsets
from .serializers import ParametersSerializer, SavePlaylistSerializer #, AddItemsToQueueSerializer


class AuthURL(APIView):
    def get(self, request, format=None):
        # TODO: ???? scopes? client_id?
        scopes = (
            'user-top-read streaming '
            'user-read-email '
            'user-read-private '
            'user-read-playback-state '
            'user-modify-playback-state '
            'user-read-currently-playing '
            'playlist-modify-private '
            'playlist-modify-public '
        )
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
    # return redirect('is_authenticated')
    return redirect('http://localhost:3000/')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        try:
            is_authenticated, access_token = is_spotify_authenticated(
                self.request.session.session_key
            )
        except Exception as e:
            return Response({'message': f'Error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        # return Response(response, status=status.HTTP_200_OK)


class UserInfo(APIView):
    def get(self, request, format=None):
        if not SpotifyToken.objects.exists():
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        token = SpotifyToken.objects.last()
        print(token.access_token)
        endpoint = "me/"
        response = execute_spotify_api_request(token, endpoint)
        print(response)

        return Response(response, status=status.HTTP_200_OK)


class PlaylistBasedOnParametersView(viewsets.ModelViewSet):
    serializer_class = ParametersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not SpotifyToken.objects.exists():
            return Response({'message': 'Unauthorized user.'}, status=status.HTTP_401_UNAUTHORIZED)
        token = SpotifyToken.objects.last()

        try:
            print(f"db songs: {Song.objects.all()}")
            delete_songs()
            print(f"db songs after delete: {Song.objects.all()}")

            top_artists_ids = get_users_top_artists(token)
            top_tracks_ids = get_users_top_tracks(token)
            tracks = get_recommendations(token,
                                         f"{top_artists_ids[0]},{top_artists_ids[2]},{top_artists_ids[3]}",
                                         f"{top_tracks_ids[1]},{top_tracks_ids[3]}")

            for track in tracks:
                Song(
                    title=track['title'],
                    artist_str=track['artist_str'],
                    duration=track['duration'],
                    image_url=track['image_url'],
                    id=track['id'],
                    uri=track['uri']
                ).save()

            print(f"db songs: {Song.objects.all()}")

        except Exception as e:
            return {'message': f'Error occurred: {e}'}

        return Response({'data': tracks}, status=status.HTTP_200_OK)


class SavePlaylistView(APIView):
    serializer_class = SavePlaylistSerializer

    def create(self, request, *args, **kwargs):
        # print("======= save playlist")
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not SpotifyToken.objects.exists():
            return Response({'message': 'Unauthorized user.'}, status=status.HTTP_401_UNAUTHORIZED)
        token = SpotifyToken.objects.last()

        try:
            # print(f"db songs: {Song.objects.all()}")
            tracks = Song.objects.all()
            save_playlist(token, tracks, request.data['name'])

        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Playlist saved successfully'}, status=status.HTTP_200_OK)


class CurrentlyPlayingSongView(APIView):
    def get(self, request, format=None):
        if not SpotifyToken.objects.exists():
            return Response({'message': 'Unauthorized user.'}, status=status.HTTP_401_UNAUTHORIZED)
        token = SpotifyToken.objects.last()

        try:
            currently_playing_song = get_currently_playing_song(token)
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if currently_playing_song is None:
            return Response({'message': 'No currently playing song.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(currently_playing_song, status=status.HTTP_200_OK)


# class PlayerQueueView(viewsets.ModelViewSet):
#     serializer_class = AddItemsToQueueSerializer
#
#     def get(self, request, format=None):
#         if not SpotifyToken.objects.exists():
#             return Response({'message': 'Unauthorized user.'}, status=status.HTTP_401_UNAUTHORIZED)
#         token = SpotifyToken.objects.last()
#
#         try:
#             player_queue = get_player_queue(token)
#         except Exception as e:
#             return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#         if player_queue is None:
#             return Response({'message': 'PLayer queue is empty.'}, status=status.HTTP_204_NO_CONTENT)
#         return Response(player_queue, status=status.HTTP_200_OK)
#
#     def post(self, request, format=None):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         if not SpotifyToken.objects.exists():
#             return Response({'message': 'Unauthorized user.'}, status=status.HTTP_401_UNAUTHORIZED)
#         token = SpotifyToken.objects.last()
#
#

