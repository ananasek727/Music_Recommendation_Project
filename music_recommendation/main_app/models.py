from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
# Create your models here.


class ImageUpload(models.Model):
    image = models.ImageField('image')

@receiver(pre_delete, sender=ImageUpload)
def image_model_pre_delete(sender, instance, **kwargs):
    # Remove the image file from the media folder
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)