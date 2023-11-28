from django.urls import path, re_path

# from .views import HomePageView
#
# urlpatterns = [
#     path('', HomePageView.as_view(), name='home_page'),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'main_app'


router = DefaultRouter()
router.register(r'images', views.ImageUploadViewSet)


urlpatterns = [
    path('', views.home_page, name='home_page'),
    # path('webcam_stream', views.webcam_stream_home_page, name='webcam_stream_home_page'),
    # path('webcam_stream/<str:pk>', views.webcam_stream, name='webcam_stream'),
    # re_path(r'^webcam_stream/(?P<pk>[\w]+)/stream/$', views.stream, name='stream_output'),
    # re_path(r'^webcam_stream/(?P<pk>[\w]+)/started/$', views.start_stream, name='start_streaming'),
    # re_path(r'^webcam_stream/(?P<pk>[\w]+)/stopped/$', views.stop_stream, name='stop_streaming'),
    path('image-upload/', views.ImageUploadView.as_view(), name='image_upload'),
    path('images/delete-all/', views.DeleteAllImagesView.as_view(), name='delete_all_images'),
    path('parameters/<str:pk>', views.parameterView, name='parameter_main'),
    re_path(r'^parameters/(?P<pk>[\w]+)/stream/$', views.stream, name='stream_output'),
    re_path(r'^parameters/(?P<pk>[\w]+)/started/$', views.start_stream, name='start_streaming'),
    re_path(r'^parameters/(?P<pk>[\w]+)/stopped/$', views.stop_stream, name='stop_streaming'),

]
urlpatterns += router.urls
