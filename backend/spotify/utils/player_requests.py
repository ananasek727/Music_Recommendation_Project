from typing import Union
from urllib.parse import urlencode

from .execute_spotify_request import execute_spotify_api_request, RequestType


def get_currently_playing_song() -> Union[dict, None]:
    endpoint = "me/player/currently-playing"
    response = execute_spotify_api_request(endpoint=endpoint,
                                           request_type=RequestType.GET)
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
        response = execute_spotify_api_request(endpoint=f"{endpoint}?{request_data}",
                                               request_type=RequestType.POST)
        if 'error' in response:
            raise Exception(f"Error occurred during adding song {song_uri} to queue: {response}")


def player_next(device_id: str) -> None:
    endpoint = "me/player/next"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(endpoint=f"{endpoint}?{request_data}",
                                           request_type=RequestType.POST)
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_pause(device_id: str) -> None:
    endpoint = "me/player/pause"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(endpoint=f"{endpoint}?{request_data}",
                                           request_type=RequestType.PUT)
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_play(device_id: str) -> None:
    endpoint = "me/player/play"

    request_data = urlencode({
        'device_id': device_id
    })
    response = execute_spotify_api_request(endpoint=f"{endpoint}?{request_data}",
                                           request_type=RequestType.PUT)
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_transfer_playback(device_id: str) -> None:
    endpoint = "me/player"

    request_data = {
        'device_ids': [device_id]
    }
    response = execute_spotify_api_request(endpoint=f"{endpoint}",
                                           request_data=request_data,
                                           request_type=RequestType.PUT)
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")


def player_set_volume(volume: int) -> None:
    endpoint = "me/player/volume"

    request_data = urlencode({
        'volume_percent': volume
    })
    response = execute_spotify_api_request(endpoint=f"{endpoint}?{request_data}",
                                           request_type=RequestType.PUT)
    if 'error' in response:
        raise Exception(f"Error occurred: {response}")
