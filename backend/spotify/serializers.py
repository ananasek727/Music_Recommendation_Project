from rest_framework import serializers
from . import POPULARITY_CHOICES, PERSONALIZATION_CHOICES, EMOTIONS


class ParametersSerializer(serializers.Serializer):
    emotion = serializers.ChoiceField(choices=EMOTIONS)
    personalization = serializers.ChoiceField(choices=PERSONALIZATION_CHOICES)
    popularity = serializers.ChoiceField(choices=POPULARITY_CHOICES)
    genres = serializers.ListField(
        child=serializers.CharField(),
        max_length=3
    )

    class Meta:
        fields = ['emotion', 'personalization', 'popularity', 'genres']


class SavePlaylistSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)

    class Meta:
        fields = ['name']


# class AddItemsToQueueSerializer(serializers.Serializer):
#     device_id = serializers.CharField(max_length=100)
#     song_uris = serializers.ListField(
#         child=serializers.CharField(),
#         max_length=40
#     )
#
#     class Meta:
#         fields = ['device_id', 'song_uris']
