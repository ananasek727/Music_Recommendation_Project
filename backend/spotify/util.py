from typing import Union
from urllib.parse import urlencode
from .models import SpotifyToken, Song
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get


BASE_URL = "https://api.spotify.com/v1/"


def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    print(user_tokens)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                                   'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def delete_user_tokens() -> None:
    SpotifyToken.objects.all().delete()


def delete_songs() -> None:
    Song.objects.all().delete()


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        tokens = get_user_tokens(session_id)
        return True, tokens.access_token

    return False, None


def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(token, endpoint, post_=False, put_=False, request_data=None):
    tokens = token
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}

    if post_:
        response = post(BASE_URL + endpoint, headers=headers, json=request_data)
        # print(response.status_code)
        # print(response)
        #
        # print("POST")

    elif put_:
        response = put(BASE_URL + endpoint, headers=headers, json=request_data)
    else:
        response = get(BASE_URL + endpoint, {}, headers=headers)
        # print(response.status_code)

    if response.status_code not in [200, 201]:
        raise Exception(f"Endpoint {endpoint} response: {response.status_code}")


    # print(response.data)
    try:
        return response.json()
    except Exception as e:
        return {'message': f'Error occurred: {e}'}


def get_users_top_artists(token: str):
    endpoint = "me/top/artists"
    request_data = urlencode({
        'limit': 10
    })
    response = execute_spotify_api_request(token, f"{endpoint}?{request_data}")
    # print("\n++++++++++++++++++++++++++++++++++")
    artists_ids = []
    for artist in response['items']:
        # print(artist['id'])
        artists_ids.append(artist['id'])
    return artists_ids
    # print(response)
    # return only artst uri / seed?


def get_users_top_tracks(token: str):
    endpoint = "me/top/tracks"
    request_data = urlencode({
        'limit': 10
    })
    response = execute_spotify_api_request(token, f"{endpoint}?{request_data}")
    # print("\n++++++++++++++++++++++++++++++++++")
    # print(response)
    track_ids = []
    for track in response['items']:
        # print(track['id'])
        track_ids.append(track['id'])
    return track_ids
    # return only tracks uri / seed?


def get_recommendations(token: str, artists_seeds: str, tracks_seeds: str) -> list:
    endpoint = "recommendations"
    request_data = urlencode({
        'limit': 10,
        'market': 'PL',
        'seed_artists': artists_seeds,
        'seed_tracks': tracks_seeds
    })
    response = execute_spotify_api_request(token, f"{endpoint}?{request_data}")
    # print("\n++++++++++++++++++++++++++++++++++")
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


def get_user_id(token) -> str:
    endpoint = "me/"
    response = execute_spotify_api_request(token, endpoint)
    # print(response)
    # print(response['id'])
    return response['id']


def save_playlist(token: str, tracks: list[Song], name: str) -> None:
    user_id = get_user_id(token)

    # create playlist
    endpoint = f"users/{user_id}/playlists"
    request_data = {
        "name": name,
        "public": False
    }
    response = execute_spotify_api_request(token, post_=True, endpoint=f"{endpoint}", request_data=request_data)
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
    response = execute_spotify_api_request(token, post_=True, endpoint=f"{endpoint}", request_data=request_data)
    # print(response)
    if 'error' in response:
        raise Exception(f"Error occurred during playlist creation: {response}")

    # print("+++++++++++")


def get_currently_playing_song(token) -> Union[dict, None]:
    endpoint = "me/player/currently-playing"
    response = execute_spotify_api_request(token, endpoint)
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

#
# def get_player_queue(token):
#     endpoint = "me/player/queue"
#     response = execute_spotify_api_request(token, endpoint)
#     print(response)
#     if 'error' in response:
#         raise Exception(f"Error occurred during currently playing song retrival: {response}")
#
#