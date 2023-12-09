from django.db import models


class SpotifyToken(models.Model):
    # TODO: user, token type?
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)


class Song(models.Model):
    # TODO: max lengths??
    title = models.CharField(max_length=150)
    artist_str = models.CharField(max_length=150)
    duration = models.CharField(max_length=50)
    image_url = models.CharField(max_length=150)
    id = models.CharField(max_length=150, primary_key=True)
    uri = models.CharField(max_length=150)

