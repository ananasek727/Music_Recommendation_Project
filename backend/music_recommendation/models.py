from django.db import models

# Create your models here.


class Song(models.Model):
    # TODO: max lengths??
    title = models.CharField(max_length=150)
    artist_str = models.CharField(max_length=150)
    duration = models.IntegerField()
    image_url = models.CharField(max_length=150)
    id = models.CharField(max_length=150, primary_key=True)
    uri = models.CharField(max_length=150)
