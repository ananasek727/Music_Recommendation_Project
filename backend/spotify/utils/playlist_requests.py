from ..models import Song
from .execute_spotify_request import execute_spotify_api_request, RequestType


def get_user_id() -> str:
    endpoint = "me/"
    response = execute_spotify_api_request(endpoint=endpoint, request_type=RequestType.GET)
    return response['id']


def save_playlist(tracks: list[Song], name: str) -> None:
    user_id = get_user_id()

    # create playlist
    endpoint = f"users/{user_id}/playlists"
    request_data = {
        "name": name,
        "public": False
    }
    response = execute_spotify_api_request(endpoint=f"{endpoint}",
                                           request_data=request_data,
                                           request_type=RequestType.POST)

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
    response = execute_spotify_api_request(endpoint=f"{endpoint}",
                                           request_data=request_data,
                                           request_type=RequestType.POST)
    if 'error' in response:
        raise Exception(f"Error occurred during playlist creation: {response}")
