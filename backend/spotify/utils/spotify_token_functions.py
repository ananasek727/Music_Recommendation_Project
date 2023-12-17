import json
from datetime import timedelta

from requests import post
from django.utils import timezone

from ..models import SpotifyToken
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


def delete_spotify_tokens() -> None:
    SpotifyToken.objects.all().delete()


def get_access_token() -> str:
    spotify_token = SpotifyToken.objects.all()[0]
    return spotify_token.access_token


def get_refresh_token() -> str:
    spotify_token = SpotifyToken.objects.all()[0]
    return spotify_token.refresh_token


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
