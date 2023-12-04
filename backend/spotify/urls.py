from django.urls import path
from .views import *

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('spotify/redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view(), name='is_authenticated'),
    path('logout', Logout.as_view()),
    path('check-auth', UserInfo.as_view())
]
