from django.urls import path
from .views import EmotionFromPhotoView

urlpatterns = [
    path('get-emotion-from-photo',
         view=EmotionFromPhotoView.as_view({'post': 'create'}),
         name='get_emotion_from_photo')
]
