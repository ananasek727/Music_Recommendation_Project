import json
from typing import Union
from urllib.parse import urlencode
from .models import SpotifyToken, Song
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from requests import post, put, get


BASE_URL = "https://api.spotify.com/v1/"


def delete_spotify_tokens() -> None:
    SpotifyToken.objects.all().delete()


def delete_songs() -> None:
    Song.objects.all().delete()


def create_spotify_token(request):
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
    )

    if not str(response.status_code).startswith('2'):
        raise Exception(f"Error: {response.status_code}")

    if not request.session.exists(request.session.session_key):
        request.session.create()

    delete_spotify_tokens()

    content = json.loads(response.content.decode('utf-8'))
    SpotifyToken(
        user=request.session.session_key,
        refresh_token=content['refresh_token'],
        access_token=content['access_token'],
        expires_in=timezone.now() + timedelta(seconds=content['expires_in']),
        token_type=content['token_type']
    ).save()


def refresh_spotify_token():
    spotify_tokens = SpotifyToken.objects.all()
    if len(spotify_tokens) > 1:
        raise Exception("Too many spotify tokens saved in database.")

    if len(spotify_tokens) == 0:
        return

    spotify_token = spotify_tokens[0]

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': spotify_token.refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })

    if not str(response.status_code).startswith('2'):
        raise Exception(f"Error: {response.status_code}")

    content = json.loads(response.content.decode('utf-8'))

    spotify_token.access_token = content['access_token']
    spotify_token.expires_in = timezone.now() + timedelta(seconds=content['expires_in'])
    spotify_token.save()


def get_access_token():
    spotify_token = SpotifyToken.objects.all()[0]
    return spotify_token.access_token


def is_authenticated() -> bool:
    if not SpotifyToken.objects.exists():
        return False

    spotify_tokens = SpotifyToken.objects.all()
    if len(spotify_tokens) != 1:
        raise Exception("Too many spotify tokens saved in database.")

    spotify_token = spotify_tokens[0]
    if spotify_token.expires_in < timezone.now() + timedelta(seconds=60):
        return False

    return True


def execute_spotify_api_request(endpoint, post_=False, put_=False, request_data=None):
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + get_access_token()}

    if post_:
        response = post(BASE_URL + endpoint, headers=headers, json=request_data)
    elif put_:
        response = put(BASE_URL + endpoint, headers=headers, json=request_data)
    else:
        response = get(BASE_URL + endpoint, {}, headers=headers)

    if response.status_code not in [200, 201, 202, 204]:
        raise Exception(f"Endpoint {endpoint}, response: {response.status_code}")

    try:
        return response.json()
    except Exception as e:
        return {'message': f'Error occurred: {e}'}


def get_users_top_artists():
    endpoint = "me/top/artists"
    request_data = urlencode({
        'limit': 10
    })
    response = execute_spotify_api_request(f"{endpoint}?{request_data}")

    artists_ids = []
    for artist in response['items']:
        artists_ids.append(artist['id'])

    return artists_ids


def get_users_top_tracks():
    endpoint = "me/top/tracks"
    request_data = urlencode({
        'limit': 10
    })
    response = execute_spotify_api_request(f"{endpoint}?{request_data}")

    track_ids = []
    for track in response['items']:
        track_ids.append(track['id'])

    return track_ids


def get_recommendations(artists_seeds: str, tracks_seeds: str) -> list:
    endpoint = "recommendations"
    request_data = urlencode({
        'limit': 10,
        'market': 'PL',
        'seed_artists': artists_seeds,
        'seed_tracks': tracks_seeds
    })
    response = execute_spotify_api_request(f"{endpoint}?{request_data}")

    tracks = []
    for track in response['tracks']:
        artist_string = ""
        for i, artist in enumerate(track['artists']):
            if i > 0:
                artist_string += ", "
            name = artist['name']
            artist_string += name

        duration_seconds = int(track['duration_ms']) / 1000
        minutes, seconds = divmod(duration_seconds, 60)
        formatted_duration = "{:d}:{:02}".format(int(minutes), int(seconds))

        tracks.append({
            'title': track['name'],
            'artist_str': artist_string,
            'duration': formatted_duration,
            'image_url': track['album']['images'][0]['url'],
            'id': track['id'],
            'uri': track['uri']
        })

    return tracks
    # print(response)
    # return only artst uri / seed?


def get_user_id() -> str:
    endpoint = "me/"
    response = execute_spotify_api_request(endpoint)
    # print(response)
    # print(response['id'])
    return response['id']


def save_playlist(tracks: list[Song], name: str) -> None:
    user_id = get_user_id()

    # create playlist
    endpoint = f"users/{user_id}/playlists"
    request_data = {
        "name": name,
        "public": False
    }
    response = execute_spotify_api_request(post_=True, endpoint=f"{endpoint}", request_data=request_data)
    # print("--")
    # print(response)

    playlist_id = response['id']
    # print(playlist_id)

    # add tracks
    endpoint = f"playlists/{playlist_id}/tracks"
    # print(endpoint)
    uris = []
    for track in tracks:
        # print(track.uri)
        uris.append(track.uri)

    # print(uris)
    request_data = {
        "uris": uris
    }
    response = execute_spotify_api_request(post_=True, endpoint=f"{endpoint}", request_data=request_data)
    # print(response)
    if 'error' in response:
        raise Exception(f"Error occurred during playlist creation: {response}")

    # print("+++++++++++")


def get_currently_playing_song() -> Union[dict, None]:
    endpoint = "me/player/currently-playing"
    response = execute_spotify_api_request(endpoint)
    # print(response)
    if 'error' in response:
        raise Exception(f"Error occurred during currently playing song retrival: {response}")

    if 'item' not in response:
        return None

    item = response['item']

    artist_string = ""
    for i, artist in enumerate(item['artists']):
        if i > 0:
            artist_string += ", "
        name = artist['name']
        artist_string += name

    duration_seconds = int(item['duration_ms']) / 1000
    minutes, seconds = divmod(duration_seconds, 60)
    formatted_duration = "{:d}:{:02}".format(int(minutes), int(seconds))

    progress_seconds = int(response['progress_ms']) / 1000
    minutes, seconds = divmod(progress_seconds, 60)
    formatted_progress = "{:d}:{:02}".format(int(minutes), int(seconds))

    currently_playing_song = {
        'title': item['name'],
        'artist': artist_string,
        'duration': formatted_duration,
        'time_stamp': formatted_progress,
        'image_url': item['album']['images'][0]['url'],
        'is_playing': response['is_playing'],
        'id': item['id'],
        'uri': item['uri']
    }

    return currently_playing_song


def add_songs_to_queue(device_id: str, song_uris: list[str]):
    endpoint = "me/player/queue"

    for song_uri in song_uris:
        request_data = urlencode({
            'uri': song_uri,
            'device_id': device_id
        })
        response = execute_spotify_api_request(post_=True, endpoint=f"{endpoint}?{request_data}")
        if 'error' in response:
            raise Exception(f"Error occurred during adding song {song_uri} to queue: {response}")


def player_next(device_id: str):
    endpoint = "me/player/next"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(post_=True, endpoint=f"{endpoint}?{request_data}")
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_pause(device_id: str):
    endpoint = "me/player/pause"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(put_=True, endpoint=f"{endpoint}?{request_data}")
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_play(device_id: str):
    endpoint = "me/player/play"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(put_=True, endpoint=f"{endpoint}?{request_data}")
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_transfer_playback(device_id: str):
    endpoint = "me/player"

    request_data = {
        'device_ids': [device_id]
    }
    response = execute_spotify_api_request(put_=True, endpoint=f"{endpoint}", request_data=request_data)
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_set_volume(volume: int):
    endpoint = "me/player/volume"

    request_data = urlencode({
        'volume_percent': volume
    })
    response = execute_spotify_api_request(put_=True, endpoint=f"{endpoint}?{request_data}")
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")

