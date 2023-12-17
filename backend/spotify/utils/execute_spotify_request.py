from datetime import timedelta
from enum import Enum

from requests import post, put, get

from .constant_parameters import SPOTIFY_BASE_URL
from .spotify_token_functions import get_access_token


class RequestType(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'


def execute_spotify_api_request(endpoint: str, request_type:  RequestType, request_data: dict = None) \
        -> dict:
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + get_access_token()}

    if request_type == RequestType.GET:
        response = get(SPOTIFY_BASE_URL + endpoint, {}, headers=headers)
    elif request_type == RequestType.POST:
        response = post(SPOTIFY_BASE_URL + endpoint, headers=headers, json=request_data)
    elif request_type == RequestType.PUT:
        response = put(SPOTIFY_BASE_URL + endpoint, headers=headers, json=request_data)
    else:
        raise Exception(f"Accepted request types: get, post and put.")

    if not str(response.status_code).startswith("2"):
    
        message_str = ""
        if response.status_code == 429:  # too many requests
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
