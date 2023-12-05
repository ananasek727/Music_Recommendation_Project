from django.urls import path
from .views import *

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('spotify/redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view(), name='is_authenticated'),
    path('logout', Logout.as_view()),
    path('check-auth', UserInfo.as_view()),
    path('create-playlist-based-on-parameters',
         view=PlaylistBasedOnParametersView.as_view({'post': 'create'}),
         name='create_playlist_based_on_parameters'),
    path('save-playlist', SavePlaylistView.as_view({'post': 'create'}), name='save_playlist'),
    path('currently-playing-song', CurrentlyPlayingSongView.as_view(), name='currently_playing_song'),
    # path('player-queue', PlayerQueueView.as_view({'post': 'create', 'get': 'get'}), name='player-queue')
]
