from django.urls import path, re_path

# from .views import HomePageView
#
# urlpatterns = [
#     path('', HomePageView.as_view(), name='home_page'),
# ]

from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('webcam_stream', views.webcam_stream_home_page, name='webcam_stream_home_page'),
    path('webcam_stream/<str:pk>', views.webcam_stream, name='webcam_stream'),
    re_path(r'^webcam_stream/(?P<pk>[\w]+)/stream/$', views.stream, name='stream_output'),
    re_path(r'^webcam_stream/(?P<pk>[\w]+)/started/$', views.start_stream, name='start_streaming'),
    re_path(r'^webcam_stream/(?P<pk>[\w]+)/stopped/$', views.stop_stream, name='stop_streaming'),
]