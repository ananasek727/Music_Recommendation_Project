import json
import random
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


def create_spotify_token(request) -> None:
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


def refresh_spotify_token() -> None:
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


def get_access_token() -> str:
    spotify_token = SpotifyToken.objects.all()[0]
    return spotify_token.access_token


def get_refresh_token() -> str:
    spotify_token = SpotifyToken.objects.all()[0]
    return spotify_token.refresh_token


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


def execute_spotify_api_request(endpoint: str, post_: bool = False, put_: bool = False, request_data: dict = None) \
        -> dict:
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + get_access_token()}

    if post_:
        response = post(BASE_URL + endpoint, headers=headers, json=request_data)
    elif put_:
        response = put(BASE_URL + endpoint, headers=headers, json=request_data)
    else:
        response = get(BASE_URL + endpoint, {}, headers=headers)

    if not str(response.status_code).startswith("2"):
        message_str = ""
        if response.status_code == 429:
            retry_after_s = int(response.headers['Retry-After'])
            delta = timedelta(seconds=retry_after_s)
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            message_str = f", Retry-After: {formatted_time}"
        raise Exception(f"Endpoint {endpoint}, response: {response.status_code}{message_str}")

    try:
        return response.json()
    except Exception as e:
        return {'message': f'Error occurred: {e}'}


def get_users_top_artists(limit=10, offset=0) -> list:
    endpoint = "me/top/artists"
    request_data = urlencode({
        'limit': limit,
        'offset': offset
    })
    response = execute_spotify_api_request(f"{endpoint}?{request_data}")

    artists_ids = []
    for artist in response['items']:
        artists_ids.append(artist['id'])

    return artists_ids


def get_users_top_tracks(limit=10, offset=0) -> list:
    endpoint = "me/top/tracks"
    request_data = urlencode({
        'limit': limit,
        'offset': offset
    })
    response = execute_spotify_api_request(f"{endpoint}?{request_data}")

    track_ids = []
    for track in response['items']:
        track_ids.append(track['id'])

    return track_ids


def get_top_artist_rand(min_index: int, max_index: int) -> str:
    artist_ids = get_users_top_artists(max_index-min_index+1, min_index)
    rand_id = random.randint(0, max_index-min_index)
    return artist_ids[rand_id]


def get_top_track_rand(min_index: int, max_index: int) -> str:
    track_ids = get_users_top_tracks(max_index - min_index + 1, min_index)
    rand_id = random.randint(0, max_index - min_index)
    return track_ids[rand_id]


def get_top_artists_rand_seed(indexes: list[(int, int)]) -> str:
    artist_ids = []
    for min_index, max_index in indexes:
        artist_ids.append(get_top_artist_rand(min_index, max_index))

    return ','.join(artist_ids)


def get_top_tracks_rand_seed(indexes: list[(int, int)]) -> str:
    tracks_ids = []
    for min_index, max_index in indexes:
        tracks_ids.append(get_top_track_rand(min_index, max_index))

    return ','.join(tracks_ids)


# def get_rand_genres_seed(num_of_genre_seeds: int) -> str:
#     endpoint = "recommendations/available-genre-seeds"
#     response = execute_spotify_api_request(endpoint)
#     selected_genres = random.sample(response['genres'], min(num_of_genre_seeds, len(response['genres'])))
#     return ','.join(selected_genres)


def set_popularity_range(parameters: dict, data: dict) -> None:
    # popularity_mapping = {
    #     'mainstream': (80, 100),
    #     'medium': (40, 85),
    #     'low': (10, 40)
    # }
    #
    # data['min_popularity'], data['max_popularity'] = popularity_mapping[parameters['popularity']]

    popularity_mapping = {
        'mainstream': 100,
        'medium': 70,
        'low': 20
    }

    data['target_popularity'] = popularity_mapping[parameters['popularity']]


def set_genre_seeds(parameters: dict, data: dict) -> None:
    # if not parameters['genres']:
    #     if parameters['personalization'] == 'low':
    #         data['seed_genres'] = get_rand_genres_seed(5)
    #     return

    data['seed_genres'] = ','.join(parameters['genres'])


def set_artists_and_songs_seeds(parameters: dict, data: dict) -> None:
    num_of_top_artists = len(get_users_top_artists(50, 0))
    art_nums = sorted(random.sample(range(num_of_top_artists), 10))

    num_of_top_tracks = len(get_users_top_tracks(50, 0))
    track_nums = sorted(random.sample(range(num_of_top_tracks), 15))

    if parameters['personalization'] == 'high':
        if len(parameters['genres']) == 3:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[0], art_nums[2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[0], track_nums[2])])
        elif len(parameters['genres']) == 2:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[0], art_nums[2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[0], track_nums[2]),
                                                            (track_nums[3], track_nums[4])])
        elif len(parameters['genres']) == 1:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[0], art_nums[1]),
                                                              (art_nums[2], art_nums[3])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[0], track_nums[2]),
                                                            (track_nums[3], track_nums[4])])
        # elif len(parameters['genres']) == 0:
        #     data['seed_artists'] = get_top_artists_rand_seed([(art_nums[0], art_nums[1]),
        #                                                       (art_nums[2], art_nums[3])])
        #     data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[0], track_nums[1]),
        #                                                     (track_nums[2], track_nums[3]),
        #                                                     (track_nums[4], track_nums[5])])

    elif parameters['personalization'] == 'medium':
        if len(parameters['genres']) == 3:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[-4], art_nums[-2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[-7], track_nums[-2])])
        elif len(parameters['genres']) == 2:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[-4], art_nums[-2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[-7], track_nums[-3]),
                                                            (track_nums[-2], track_nums[-1])])
        elif len(parameters['genres']) == 1:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[-4], art_nums[-2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[-7], track_nums[-5]),
                                                            (track_nums[-4], track_nums[-3]),
                                                            (track_nums[-2], track_nums[-1])])
        # elif len(parameters['genres']) == 0:
        #     data['seed_artists'] = get_top_artists_rand_seed([(art_nums[-5], art_nums[-3]),
        #                                                       (art_nums[-2], art_nums[-1])])
        #     data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[-7], track_nums[-5]),
        #                                                     (track_nums[-4], track_nums[-3]),
        #                                                     (track_nums[-2], track_nums[-1])])


def set_emotion_parameters(emotion: str, data: dict) -> None:
    data['max_liveness'] = 0.8

    if emotion == 'angry':
        # data.update({'min_energy': 0.6, 'max_energy': 1, 'target_energy': 0.8})
        # data.update({'min_valence': 0.6, 'max_valence': 1, 'target_valence': 0.8})
        # # data.update({'min_loudness': '-60', 'max_loudness': '-20', 'target_loudness': -45})
        # data.update({'min_mode': 0, 'max_mode': 0, 'target_mode': 0})
        # data.update({'min_key': 6, 'max_key': 11})
        # data.update({'min_tempo': 100})
        data.update({'target_energy': 0.8})
        data.update({'target_valence': 0.8})
        data.update({'target_loudness': -40})
        data.update({'target_mode': 0})
        data.update({'target_key': 9})
        data.update({'target_tempo': 140})

    elif emotion == 'disgust':
        # data.update({'min_energy': 0.5, 'max_energy': 0.8, 'target_energy': 0.65})
        # data.update({'min_valence': 0, 'max_valence': 0.4, 'target_valence': 0.1})
        # data.update({'min_mode': 0, 'max_mode': 0, 'target_mode': 0})
        # data.update({'max_tempo': 100})
        data.update({'target_energy': 0.65})
        data.update({'target_valence': 0.15})
        data.update({'target_mode': 0})
        data.update({'target_tempo': 60})

    elif emotion == 'fear':
        # data.update({'min_energy': 0.5, 'max_energy': 0.95, 'target_energy': 0.75})
        # data.update({'min_valence': 0, 'max_valence': 0.4, 'target_valence': 0.2})
        # # data.update({'min_loudness': -15, 'max_loudness': 0, 'target_loudness': -7})
        # data.update({'min_key': 6, 'max_key': 11})
        # data.update({'min_tempo': 100})
        data.update({'target_energy': 0.7})
        data.update({'target_valence': 0.2})
        data.update({'target_loudness': -7})
        data.update({'target_key': 9})
        data.update({'target_tempo': 140})

    elif emotion == 'happy':
        # data.update({'min_energy': 0.6, 'max_energy': 1, 'target_energy': 0.8})
        # data.update({'min_valence': 0.6, 'max_valence': 1, 'target_valence': 0.95})
        # data.update({'min_mode': 1, 'max_mode': 1, 'target_mode': 1})
        # data.update({'min_key': 0, 'max_key': 6})
        # data.update({'min_tempo': 100})
        data.update({'target_energy': 0.8})
        data.update({'target_valence': 0.95})
        data.update({'target_mode': 1})
        data.update({'target_key': 3})
        data.update({'target_tempo': 120})

    elif emotion == 'neutral':
        # data.update({'min_energy': 0, 'max_energy': 0.5})
        # data.update({'min_valence': 0.3, 'max_valence': 0.8})
        # # data.update({'min_loudness': -10, 'max_loudness': 0, 'target_loudness': -3})
        # data.update({'min_key': 0, 'max_key': 7})
        # data.update({'min_tempo': 20, 'max_tempo': 100})
        data.update({'target_energy': 0.25})
        data.update({'target_valence': 0.5})
        data.update({'target_loudness': -3})
        data.update({'target_key': 4})
        data.update({'target_tempo': 65})

    elif emotion == 'sad':
        # data.update({'min_energy': 0.1, 'max_energy': 0.6})
        # data.update({'min_valence': 0, 'max_valence': 0.3})
        # # data.update({'min_loudness': -15, 'max_loudness': 0, 'target_loudness': -7})
        # data.update({'min_mode': 0, 'max_mode': 0, 'target_mode': 0})
        # data.update({'min_key': 0, 'max_key': 6})
        # data.update({'max_tempo': 100})
        data.update({'target_energy': 0.3})
        data.update({'target_valence': 0})
        data.update({'target_loudness': -5})
        data.update({'target_mode': 0})
        data.update({'target_key': 2})
        data.update({'target_tempo': 70})

    elif emotion == 'surprise':
        # data.update({'min_energy': 0.4, 'max_energy': 0.8, 'target_energy': 0.6})
        # data.update({'min_valence': 0.1, 'max_valence': 0.3, 'target_valence': 0.2})
        # data.update({'min_key': 6, 'max_key': 11})
        # data.update({'min_tempo': 100})
        data.update({'target_energy': 0.6})
        data.update({'target_valence': 0.2})
        data.update({'target_key': 8})
        data.update({'target_tempo': 130})


def get_recommendation_request_parameters(parameters) -> dict:
    data = {
        'limit': 10,
        'market': 'PL'
    }

    set_popularity_range(parameters, data)
    set_genre_seeds(parameters, data)
    set_artists_and_songs_seeds(parameters, data)

    set_emotion_parameters(parameters['emotion'], data)

    return data


def get_recommendations(parameters) -> list:
    endpoint = "recommendations"

    tracks = []
    # tries = 0
    # while len(tracks) < 10 or tries < 5:
    #     tries += 1
    request_data = urlencode(get_recommendation_request_parameters(parameters))
    response = execute_spotify_api_request(f"{endpoint}?{request_data}")

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


def get_user_id() -> str:
    endpoint = "me/"
    response = execute_spotify_api_request(endpoint)
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

    playlist_id = response['id']

    # add tracks
    endpoint = f"playlists/{playlist_id}/tracks"
    uris = []
    for track in tracks:
        uris.append(track.uri)

    # save playlist
    request_data = {
        "uris": uris
    }
    response = execute_spotify_api_request(post_=True, endpoint=f"{endpoint}", request_data=request_data)
    if 'error' in response:
        raise Exception(f"Error occurred during playlist creation: {response}")


def get_currently_playing_song() -> Union[dict, None]:
    endpoint = "me/player/currently-playing"
    response = execute_spotify_api_request(endpoint)
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


def add_songs_to_queue(device_id: str, song_uris: list[str]) -> None:
    endpoint = "me/player/queue"

    for song_uri in song_uris:
        request_data = urlencode({
            'uri': song_uri,
            'device_id': device_id
        })
        response = execute_spotify_api_request(post_=True, endpoint=f"{endpoint}?{request_data}")
        if 'error' in response:
            raise Exception(f"Error occurred during adding song {song_uri} to queue: {response}")


def player_next(device_id: str) -> None:
    endpoint = "me/player/next"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(post_=True, endpoint=f"{endpoint}?{request_data}")
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_pause(device_id: str) -> None:
    endpoint = "me/player/pause"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(put_=True, endpoint=f"{endpoint}?{request_data}")
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_play(device_id: str) -> None:
    endpoint = "me/player/play"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(put_=True, endpoint=f"{endpoint}?{request_data}")
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_transfer_playback(device_id: str) -> None:
    endpoint = "me/player"

    request_data = {
        'device_ids': [device_id]
    }
    response = execute_spotify_api_request(put_=True, endpoint=f"{endpoint}", request_data=request_data)
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_set_volume(volume: int) -> None:
    endpoint = "me/player/volume"

    request_data = urlencode({
        'volume_percent': volume
    })
    response = execute_spotify_api_request(put_=True, endpoint=f"{endpoint}?{request_data}")
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")
