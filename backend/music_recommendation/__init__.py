import os
import tensorflow
import cv2
import warnings

# Ignore all warnings globally
warnings.filterwarnings("ignore")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../static/model")
PROTOTXT_PATH = os.path.join(os.path.dirname(__file__), "../static/deploy.prototxt")
FR_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../static/res10_300x300_ssd_iter_140000_fp16.caffemodel")
CONFIDENCE = 0.7

net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, FR_MODEL_PATH)

assert isinstance(tensorflow.keras.models, object)
emotion_model = tensorflow.keras.models.load_model(MODEL_PATH)

# PERSONALIZATION_CHOICES = ['high', 'medium', 'low']
# POPULARITY_CHOICES = ['mainstream', 'medium', 'low']
# EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
