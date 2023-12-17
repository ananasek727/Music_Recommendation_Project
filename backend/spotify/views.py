from django.shortcuts import redirect
from requests import Request
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import SpotifyToken, Song
from .serializers import (ParametersSerializer, SavePlaylistSerializer, AddItemsToQueueSerializer, DeviceIdSerializer,
                          VolumeSerializer)
from .utils.credentials import REDIRECT_URI, CLIENT_ID
from .utils.constant_parameters import SCOPES
from .utils.execute_spotify_request import execute_spotify_api_request, RequestType
from .utils.spotify_token_functions import (delete_spotify_tokens, create_spotify_token, refresh_spotify_token,
                                            get_refresh_token, get_access_token, is_authenticated)
from .utils.song_functions import delete_songs
from .utils.player_requests import (get_currently_playing_song, add_songs_to_queue, player_next, player_pause,
                                    player_play, player_transfer_playback, player_set_volume)
from .utils.playlist_requests import save_playlist
from .utils.recommendation_requests import get_recommendations


class AuthURL(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': SCOPES,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    create_spotify_token(request)
    return redirect('http://localhost:3000/')


class IsAuthenticated(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        try:
            return Response({'is_authenticated': is_authenticated()}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': f'Error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccessToken(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        try:
            if not is_authenticated():
                return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'access_token': get_access_token(),
                                 'refresh_token': get_refresh_token()}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': f'Error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RefreshToken(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        if not SpotifyToken.objects.exists():
            return Response({'message': 'User not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh_spotify_token()
        except Exception as e:
            return Response({'message': f'Error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Token successfully refreshed.'}, status=status.HTTP_200_OK)


class Logout(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        if not SpotifyToken.objects.exists():
            return Response({'message': 'User not logged in.'}, status=status.HTTP_200_OK)

        try:
            delete_spotify_tokens()
        except Exception as e:
            return Response({'message': f'Error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Successfully logged out of Spotify.',
                         'url': 'https://www.spotify.com/fr/logout'}, status=status.HTTP_200_OK)


class UserInfo(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            endpoint = "me/"
            response = execute_spotify_api_request(endpoint=endpoint, request_type=RequestType.GET)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaylistBasedOnParametersView(viewsets.ModelViewSet):
    serializer_class = ParametersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            delete_songs()

            tracks = get_recommendations(request.data)
            for track in tracks:
                Song(
                    title=track['title'],
                    artist_str=track['artist_str'],
                    duration=track['duration'],
                    image_url=track['image_url'],
                    id=track['id'],
                    uri=track['uri']
                ).save()

        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': tracks}, status=status.HTTP_200_OK)


class SavePlaylistView(viewsets.ModelViewSet):
    serializer_class = SavePlaylistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            tracks = Song.objects.all()
            save_playlist(tracks, request.data['name'])

        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Playlist saved successfully.'}, status=status.HTTP_200_OK)


class CurrentlyPlayingSongView(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            currently_playing_song = get_currently_playing_song()
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if currently_playing_song is None:
            return Response({'message': 'No currently playing song.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(currently_playing_song, status=status.HTTP_200_OK)


class PlayerQueueView(viewsets.ModelViewSet):
    serializer_class = AddItemsToQueueSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            add_songs_to_queue(request.data['device_id'], request.data['song_uris'])
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'Songs successfully added to queue.'}, status=status.HTTP_200_OK)


class PlayerNextView(viewsets.ModelViewSet):
    serializer_class = DeviceIdSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            player_next(request.data['device_id'])
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'Command sent.'}, status=status.HTTP_200_OK)


class PlayerPauseView(viewsets.ModelViewSet):
    serializer_class = DeviceIdSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            player_pause(request.data['device_id'])
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'Command sent.'}, status=status.HTTP_200_OK)


class PlayerPlayView(viewsets.ModelViewSet):
    serializer_class = DeviceIdSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            player_play(request.data['device_id'])
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'Command sent.'}, status=status.HTTP_200_OK)


class PlayerTransferPlaybackView(viewsets.ModelViewSet):
    serializer_class = DeviceIdSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            player_transfer_playback(request.data['device_id'])
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'Command sent.'}, status=status.HTTP_200_OK)


class PlayerSetVolumeView(viewsets.ModelViewSet):
    serializer_class = VolumeSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            player_set_volume(request.data['volume_percent'])
        except Exception as e:
            return Response({'message': f'Error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'Volume set to {request.data["volume_percent"]}%.'}, status=status.HTTP_200_OK)
