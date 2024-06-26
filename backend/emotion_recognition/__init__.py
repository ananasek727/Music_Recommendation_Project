import os
import tensorflow
import cv2

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../static/model")
PROTOTXT_PATH = os.path.join(os.path.dirname(__file__), "../static/deploy.prototxt")
FR_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../static/res10_300x300_ssd_iter_140000_fp16.caffemodel")
CONFIDENCE = 0.7

net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, FR_MODEL_PATH)

assert isinstance(tensorflow.keras.models, object)
emotion_model = tensorflow.keras.models.load_model(MODEL_PATH)
