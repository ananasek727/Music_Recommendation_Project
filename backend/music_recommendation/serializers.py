from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import base64
import binascii
# from . import POPULARITY_CHOICES, PERSONALIZATION_CHOICES, EMOTIONS


def validate_base64(value):
    try:
        base64.b64decode(value.split(',')[1])
    except (TypeError, binascii.Error):
        raise ValidationError("Invalid base64 format")


class PhotoRequestSerializer(serializers.Serializer):
    base64_photo = serializers.CharField(
        required=True,
        validators=[validate_base64]
    )

    class Meta:
        fields = ['base64_photo']


# class ParametersSerializer(serializers.Serializer):
#     emotion = serializers.ChoiceField(choices=EMOTIONS)
#     personalization = serializers.ChoiceField(choices=PERSONALIZATION_CHOICES)
#     popularity = serializers.ChoiceField(choices=POPULARITY_CHOICES)
#     genres = serializers.ListField(
#         child=serializers.CharField(),
#         max_length=5
#     )
#
#     class Meta:
#         fields = ['emotion', 'personalization', 'popularity', 'genres']
#
