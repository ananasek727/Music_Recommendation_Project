from django.urls import path
from .views import EmotionFromPhotoView #, PlaylistBasedOnParametersView

urlpatterns = [
    path('get-emotion-from-photo',
         view=EmotionFromPhotoView.as_view({'post': 'create'}),
         name='get_emotion_from_photo'),
    # path('create-playlist-based-on-parameters',
    #      view=PlaylistBasedOnParametersView.as_view({'post': 'create'}),
    #      name='create_playlist_based_on_parameters')
]
