from django.urls import path
from .views import (AuthURL, spotify_callback, IsAuthenticated, AccessToken, RefreshToken, Logout, UserInfo,
                    PlaylistBasedOnParametersView, SavePlaylistView, CurrentlyPlayingSongView, PlayerQueueView,
                    PlayerNextView, PlayerPauseView, PlayerPlayView, PlayerTransferPlaybackView, PlayerSetVolumeView)

urlpatterns = [
    path('get-auth-url', AuthURL.as_view({'get': 'list'}), name='get_auth_url'),
    path('spotify/redirect', spotify_callback, name='spotify_redirect'),
    path('is-authenticated', IsAuthenticated.as_view({'get': 'list'}), name='is_authenticated'),
    path('access-token', AccessToken.as_view({'get': 'list'}), name='access_token'),
    path('token-refresh', RefreshToken.as_view({'get': 'list'}), name='token_refresh'),
    path('logout', Logout.as_view({'delete': 'destroy'}), name='logout'),
    path('check-auth', UserInfo.as_view({'get': 'list'}), name='check_auth'),
    path('create-playlist-based-on-parameters',
         view=PlaylistBasedOnParametersView.as_view({'post': 'create'}),
         name='create_playlist_based_on_parameters'),
    path('save-playlist', SavePlaylistView.as_view({'post': 'create'}), name='save_playlist'),
    path('currently-playing-song', CurrentlyPlayingSongView.as_view({'get': 'list'}), name='currently_playing_song'),
    path('player/queue', PlayerQueueView.as_view({'post': 'create'}), name='player_queue'),
    path('player/next', PlayerNextView.as_view({'post': 'create'}), name='player_next'),
    path('player/pause', PlayerPauseView.as_view({'put': 'update'}), name='player_pause'),
    path('player/play', PlayerPlayView.as_view({'put': 'update'}), name='player_play'),
    path('player/tranfer-playback', PlayerTransferPlaybackView.as_view({'put': 'update'}),
         name='player_transfer_playback'),
    path('player/set-volume', PlayerSetVolumeView.as_view({'put': 'update'}),
         name='player_set_volume'),
]
