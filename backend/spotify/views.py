from django.shortcuts import redirect
from .util import (execute_spotify_api_request, delete_spotify_tokens, create_spotify_token,
                   get_recommendations, delete_songs, save_playlist, get_currently_playing_song, add_songs_to_queue,
                   player_next, player_pause, player_play, player_transfer_playback, player_set_volume,
                   refresh_spotify_token, is_authenticated, get_access_token)
from .credentials import REDIRECT_URI, CLIENT_ID
from rest_framework.views import APIView
from requests import Request
from rest_framework.response import Response
from rest_framework import status
from .models import SpotifyToken, Song
from rest_framework import viewsets
from .serializers import (ParametersSerializer, SavePlaylistSerializer, AddItemsToQueueSerializer, DeviceIdSerializer,
                          VolumeSerializer)


class AuthURL(APIView):
    def get(self, request, format=None):
        # TODO: scopes -> gdzies indziej trzymac
        scopes = (
            'user-top-read '
            'streaming '
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
                return Response({'message:' 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'access_token': get_access_token()}, status=status.HTTP_200_OK)

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


class Logout(APIView):
    def delete(self, request, format=None):
        if not SpotifyToken.objects.exists():
            return Response({'message': 'User not logged in.'}, status=status.HTTP_200_OK)

        try:
            delete_spotify_tokens()
        except Exception as e:
            return Response({'message': f'Error occurred: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Successfully logged out of Spotify.',
                         'url': 'https://www.spotify.com/fr/logout'}, status=status.HTTP_200_OK)


class UserInfo(APIView):
    def get(self, request, format=None):
        if not is_authenticated():
            return Response({'message': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        endpoint = "me/"
        response = execute_spotify_api_request(endpoint)

        return Response(response, status=status.HTTP_200_OK)


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
            # print(request.data)
            # request_data = get_recommendation_request_parameters(request.data)
            # get_recommendations(request)

            # top_artists_ids = get_users_top_artists()
            # top_tracks_ids = get_users_top_tracks()
            # tracks = get_recommendations(f"{top_artists_ids[0]},{top_artists_ids[2]},{top_artists_ids[3]}",
            #                              f"{top_tracks_ids[1]},{top_tracks_ids[3]}")
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

            # print(f"db songs: {Song.objects.all()}")

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

        return Response({'message': 'Playlist saved successfully'}, status=status.HTTP_200_OK)


class CurrentlyPlayingSongView(APIView):
    def get(self, request, format=None):
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
