import base64
import binascii

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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