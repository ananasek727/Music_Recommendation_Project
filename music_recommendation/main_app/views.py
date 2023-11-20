from django.shortcuts import redirect, render
import os
import shutil
import numpy as np
import time
import cv2
import tensorflow as tf
from django.http import StreamingHttpResponse, HttpResponse
from django.template import loader
from imutils.video import FPS
from rest_framework import viewsets
from .models import ImageUpload
from .serializers import ImageUploadSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
# Create your views here.


# class HomePageView(View):
#     # context_object_name = 'home_page'
#     # template_name = 'music_recommendation/home_page.html'
#
#     def get(self, request):
#         return render(request, "music_recommendation/home_page.html")
#

from django.http import HttpResponse
frame = None
vc = None

# fps counter
fps = FPS()
CONFIDENCE = 0.7

# paths for models loading
PROTOTXT_PATH = os.path.join(os.path.dirname(__file__), "../static/deploy.prototxt.txt")
FR_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../static/res10_300x300_ssd_iter_140000.caffemodel")
Emotion_MODEL_PATH_CNN = os.path.join(os.path.dirname(__file__), "../static/model2_CNN")
Emotion_MODEL_PATH_MobileNetV3Large = os.path.join(os.path.dirname(__file__), "model\models\model2_MobileNetV3Large").replace('\\music_recommendation\\main_app\\','\\')
Emotion_MODEL_PATH_ResNet50 = os.path.join(os.path.dirname(__file__), "model\models\model1_ResNet50").replace('\\music_recommendation\\main_app\\','\\')
# load classification model
net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, FR_MODEL_PATH)

# load pre-trained models
assert isinstance(tf.keras.models, object)
emotionModel_CNN = tf.keras.models.load_model(Emotion_MODEL_PATH_CNN)
emotionModel_MobileNetV3Large = tf.keras.models.load_model(Emotion_MODEL_PATH_MobileNetV3Large)
emotionModel_ResNet50 = tf.keras.models.load_model(Emotion_MODEL_PATH_ResNet50)
#
#
# ##
chosenModel = ""
# ##


def home_page(request):
    return render(request, 'music_recommendation/home_page.html', None)

def parameterView(request, pk):
    return render(request, 'music_recommendation/choose_parameters.html', context={ "pk": pk})

# def webcam_stream_home_page(request):
#     return render(request, 'music_recommendation/webcam_stream_home_page.html')


def webcam_stream(request, pk):
    global chosenModel
    chosenModel = pk
    template = loader.get_template('music_recommendation/webcam_stream.html')
    context = {
        'stream_started': False
    }
    return HttpResponse(template.render(context, request))


def stream(request, pk):
    return StreamingHttpResponse(stream_source(), content_type="multipart/x-mixed-replace;boundary=frame")


def start_stream(request, pk):
    template = loader.get_template('music_recommendation/choose_parameters.html')
    context = {
        'stream_started': True
    }
    return HttpResponse(template.render(context, request))


def stop_stream(request, pk):
    # global vc, fps
    global vc
    # double-checking whether the stream was launched, closing the vc
    if isinstance(vc, cv2.VideoCapture):
        vc.release()
    # fps.stop()
    # print the average fpg to the console
    # fps_num = fps.fps() if fps.fps() > 0 else 0
    # print("Average number of fps: ", fps_num)
    template = loader.get_template('music_recommendation/choose_parameters.html')
    context = {
        'stream_started': False,
        # 'fps_number': fps_num
    }
    return HttpResponse(template.render(context, request))


# function which will start generating webcam stream in our website
def stream_source():
    global vc, fps
    # start the video stream
    vc = cv2.VideoCapture(0)
    # allow our camera sensor to warm up
    time.sleep(3.0)
    # check whether camera is valid
    if not vc.isOpened():
        print("Cannot open camera. Try restarting the server.")
        return
    # start counting fps
    fps.start()
    # precaution variable to exit the loop in special cases. this may not be even needed, because exiting is handled by
    # the variable 'stream_started' passed to the view's context
    exit_counter = 0
    # loop over the frames from the video stream
    while True:
        # read frame from camera
        ret, frame_in = vc.read()

        # checks whether the frame is received properly
        if not frame_in.shape or not ret:
            print("Can't get any frames. Closing in ", 5 - exit_counter)
            exit_counter += 1

        # exits when we receive at least 5 faulty frames
        if exit_counter >= 5:
            vc.release()
            return

        # output predictions
        frame_out = process_frame(frame_in)


        # update fps counter
        fps.update()

        # convert image to jpg
        (flag, encodedImage) = cv2.imencode(".jpg", frame_out)

        # then to byte array, yield the result. this is so that it may be displayed on the website
        if flag:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')


# utility function used to remove files from specified directory
def remove_files(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# 1x7 array
def predicted_emotion(array):
    label_map = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
    return label_map[np.argmax(array)]


# utility function used to process a frame and output predictions on it.
def process_frame(frame_in):
    global chosenModel
    (h, w) = frame_in.shape[:2]

    # convert to blob (needed for detection for the Caffe model)
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame_in, (300, 300), interpolation=cv2.INTER_AREA), 1.0, (300, 300), (104.0, 117.0, 123.0)
    )

    # pass for detection
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # ignore weak detections
        if confidence < CONFIDENCE:
            continue

        # rectangle box
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # compute height and width of the frame
        width = endX - startX
        height = endY - startY

        # extract 224x224 and 100x100 face image that we will use to pass for the predictions,
        # normalize the frame so that the image is not distorted in any way
        try:
            crop_x = crop_y = 0
            if height > width:
                crop_y = height - width
            elif height < width:
                crop_x = width - height
            face_image = cv2.resize(frame_in[int(startY + 0.8 * crop_y):int(endY - 0.2 * crop_y),
                                        int(startX + 0.5 * crop_x):int(endX - 0.5 * crop_x)], (224, 224),
                                        interpolation=cv2.INTER_AREA)
        except Exception as e:
            print("Caught exception: ", e)
            continue

        # expand frame dimensions to fit it into models
        # face_image = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY)
        # face_image = face_image.reshape((1,) + face_image.shape)

        # use selected model
        # if chosenModel == "CNN":
        if True:
                face_image = cv2.resize(face_image, (48, 48))
                face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
                face_image = face_image.reshape((1, 48, 48, 1))
                predict_emotion_model = predicted_emotion(emotionModel_CNN.predict(x=face_image, verbose=0))
        # elif chosenModel == "MobileNetV3Large":
        #         face_image = np.expand_dims(face_image, axis=0)
        #         predict_emotion_model = predicted_emotion(emotionModel_MobileNetV3Large.predict(x=face_image, verbose=0))
        # elif chosenModel == "ResNet50":
        #         face_image = np.expand_dims(face_image, axis=0)
        #         predict_emotion_model = predicted_emotion(emotionModel_ResNet50.predict(x=face_image, verbose=0))


        #predict_emotion_model_1 = emotionModel_1.predict(x=face_image, verbose=0)[0][0]

        # print out text
        (tFace, tScale, tColor, tThickness) = (cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 0, 255), 1)
        text1 = "C:{certainty:.2f}%  Emotion:{emotion}".format(certainty=confidence * 100, emotion=str(predict_emotion_model))
        (_, offset), _ = cv2.getTextSize(text1, tFace, tScale, tThickness)
        y1 = startY - offset if startY - offset > offset else startY + offset

        cv2.rectangle(frame_in, (startX, startY), (endX, endY), tColor, 2)
        cv2.putText(
            frame_in, text1, (startX, y1), tFace, tScale, tColor, tThickness
        )
    return frame_in


class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer


class ImageUploadView(TemplateView):
    template_name = "music_recommendation/image_upload.html"


class DeleteAllImagesView(APIView):
    def delete(self, request):
        try:
            ImageUpload.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)