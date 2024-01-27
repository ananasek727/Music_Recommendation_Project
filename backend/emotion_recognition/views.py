import cv2
import numpy as np
import base64

from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import PhotoRequestSerializer
from . import CONFIDENCE, net, emotion_model

# Create your views here.


def get_face_photo_from_base64_image(base64_image: str) -> np.array:
    image_data = base64_image.split(',')[1]
    image_binary = base64.b64decode(image_data)

    image_array = cv2.imdecode(np.frombuffer(image_binary, np.uint8), cv2.IMREAD_COLOR)
    if image_array is None:
        raise Exception("Incorrect image encoding.")

    (h, w) = image_array.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image_array, (300, 300), interpolation=cv2.INTER_AREA), 1.0, (300, 300),
        (104.0, 117.0, 123.0), False, False
    )

    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < CONFIDENCE:
            continue

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        width = endX - startX
        height = endY - startY

        crop_x = crop_y = 0
        if height > width:
            crop_y = height - width
        elif height < width:
            crop_x = width - height

        new_start_y = int(startY + 0.8 * crop_y)
        new_end_y = int(endY - 0.2 * crop_y)
        new_start_x = int(startX + 0.5 * crop_x)
        new_end_x = int(endX - 0.5 * crop_x)

        cropped_image_array = image_array[new_start_y:new_end_y, new_start_x:new_end_x]

        face_image = cv2.resize(cropped_image_array,
                                (48, 48),
                                interpolation=cv2.INTER_AREA)

        return face_image

    raise Exception("No face detected.")


def predicted_emotion(array):
    label_map = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
    return label_map[np.argmax(array)]


def get_emotion_from_image(image: np.array) -> str:
    face_image = cv2.resize(image, (48, 48))
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_image = face_image.reshape((1, 48, 48, 1))
    emotion = predicted_emotion(emotion_model.predict(x=face_image, verbose=0))
    return str(emotion)


class EmotionFromPhotoView(viewsets.ModelViewSet):
    serializer_class = PhotoRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            face_photo = get_face_photo_from_base64_image(request.data['base64_photo'])
            emotion = get_emotion_from_image(face_photo)
        except Exception as e:
            return Response({'message': f'Error: {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'emotion': emotion}, status=status.HTTP_200_OK)
