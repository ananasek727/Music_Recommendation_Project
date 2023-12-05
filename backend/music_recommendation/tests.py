from django.test import TestCase, RequestFactory
from .views import EmotionFromPhotoView, PlaylistBasedOnParametersView

# Create your tests here.


class EmotionFromPhotoTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.correct_base64_image = (
            "data:image/jpeg;base64,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")

    def test_invalid_request(self):
        request_data = {}
        request = self.factory.post('get_emotion_from_photo', request_data)
        response = EmotionFromPhotoView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.data['message'])

    def test_get_emotion_from_base64_image(self):
        request_data = {"base64_photo": self.correct_base64_image}
        request = self.factory.post('get_emotion_from_photo', request_data)
        response = EmotionFromPhotoView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['emotion'] in ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'])

    def test_incorrect_base_64_image_fail(self):
        base64_image = ("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgU"
                        "GBgYFBgpr8sPjp8R4/iz8dtf8cWsu6ymvTDYnt9niGxT+IXd/wKuV8kySMhGV38DHYmp/gY2s6B8X9I1iwuH"
                        "hkt7/AOSaJtrDqMgiv1b+EnxI1S58OW9p4mR57Z4xmaMZaP3x6ewr2vwh4W+Hraf/AGqlzG8gUMjqFUNn6DP1FfLn/BUv4"
                        "/6V4H+Fknw78B6jGuo6sGjujbHmCArhzkdGb7o9ia/MmGCW3t3jQDlCgx9Mmv/Z")

        request_data = {"base64_photo": base64_image}
        request = self.factory.post('get_emotion_from_photo', request_data)
        response = EmotionFromPhotoView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Incorrect image encoding', response.data['message'])

    def test_detect_face_in_image_fail(self):
        base64_image = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAhCAYAAABeD2IVAAAAAXNSR0IArs4c6QAAAARnQU1B"
                        "AACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAVtSURBVFhHpZjLb1VVFIfXPfe29MFjDMQERjIzDvwHYAbBqRN5jB"
                        "0xcmCUxKEzY0yMKRMGGgcmxAGMbAwhhnRgtTEaotC0QrxNKiJS2kt7H+5vn363m+Nj4i9ZrLXX87fXOfe2pXXs2LFRNFBV"
                        "VfT7/Wi32/k8Go2i1WqN9XA4zDE0IJ+YwE8e0G8O2jrO9LGvM1JONU4oG+G3gQUCvw3QDgHWCoaaK4hz7nQ6+fKAHvYZV5"
                        "NAYlk8GAzGDSkwhi6bgZI0IKckLlGHM4/+zjUXX87EwQGUtwTELHBDCLa5xEpynNkQPbGBGpDjpYTx3JdDWYi4IRL0aRvD"
                        "BhITuWkShrIFYb6gR9nHS4FMysZoEn0P3F5ZjF02AOQDchQfi37q7KMf4HOuSOe9T0M5EO2w0gYOAA6wsfXNwZIhT1/pL2"
                        "srDBNAmWgScGv4S20zc8te5EDCfvqA+Z6Bs6t/IwFsDsxxqHXGylxgjJ6+Ds0tcdHySY3zTAI0Iolg2aBsiqZJSbCJMoZ4"
                        "Lut8HTgL7fGnTxLARwWI0UxCFmIDb6utH5iLnx6SkVyJ8pwfH8BJc4sRfKWtiPJMjvWeES8Eyny0OQpAjx9fyR5dbou4Zw"
                        "Y4xGbW428O9TH5CuhHU3PkyJGYm5uLxcXFWF5ejnv37kXr+PHjKb6XiDjUQc2BJfD/nx/ely5dinPnzsXNmzdjaWkp0i8I"
                        "kX9LkETZUFuwqeZghzpI4Wwf4vbhTI9m7uHDh2NtbW3PVxYg5Y200XxDO6CMATYlCR8Tcc76JQqs5Yx0u93xfJC/PNmChc"
                        "BkmzQ1uT4S87Dx2QuUdcTpb60x8xF8WfP4TMDhFvDZrAn85PkumaNtPdqLAnwOB5I8evRonDp1KvuzfuvKj6Nr778evaeP"
                        "ciKwuGyg9lPY9ANsCemXMChr6K194cKFuHz5cj6D1ofXfx9tbm7FtY/eiO7y0q57r4EoCWJ7S2FMEuYjfNRLrKysxMmTJ5"
                        "/rRx2bPnPmTLSufvXHaHtnFBsbT+Ljd16NrY16YxSUwzljU8wZoQlaWIN2Y+DixYtjP3p9fT1u3LiRY8AYwpNofX77z1G/"
                        "P4rtJA9Wf4q5d1/bTa2TGUyihCSp+B5JAB8gj7r/igNiwHjOvb6YSKXX5OHj7Vh72Ivvv12I7d5mPFq7G90787H56P5zjU"
                        "ty6NIvUQegOZsPODdz7TGu++zWb6OVXzdj89kg+gP+IID5KJ7tDKOXfOsP7sTdr6/E4+4P4yIJgbJpOcxYObi5dc7z8/PR"
                        "6/ViYWEhVldX62/0D764n3sM0oz6MdakdpLubQ9jqzeMja2d+Pn2J/HLN5/mYQ6nMbaQAAIkK5pxas+fPx9nz56NEydOxP"
                        "T0dPa3rn7ZrUmlf/gDg3drmBgOUsNM6tkwnvYG8WSrH99dfy8eLt/Khd4U7TBsIGmAH1uffqAfmJd9B2aqODBbxaGZThza"
                        "307Sif3JPpDk4CzSzvrQ7ES8fPrNqDqT48ZuQhH6IV3mYku8WWMevmp2OpFAIAeRmXYiuSvYuwSxD85Oxkun3x43Btr5hu"
                        "nWEBG8Pw5TT0xM/O0CEhbV7FQ7smRy7XpLEk0ioexL+oUXXxk3pRG2DSFVEoYgcYmSZ661xsvHW03ta8dUIjWTNOQgBhE3"
                        "qK+W2idsJEl+FpbbgiCx/IW4SwBbGKcHNrWck05MkXYVkxNVzOStQbCT7Jocdq1rvxsomyIOUhtHJMpgiRlDgDVVJpRvV+"
                        "tOOk9Nps2xveekJoxmI8Atod2Q5PQDBpmjBmXcGHWJVGqWiHRy06TTxjpJQ4zNzOxLG0syPYmkR5226UB0+WXoBtT/9D8q"
                        "2AqXoA6g6/97iPgL+Jk1/hkNl90AAAAASUVORK5CYII=")

        request_data = {"base64_photo": base64_image}
        request = self.factory.post('get_emotion_from_photo', request_data)
        response = EmotionFromPhotoView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn('No face detected', response.data['message'])

#
# class PlaylistBasedOnParametersTestCase(TestCase):
#
#     def setUp(self):
#         self.factory = RequestFactory()
#
#     def test_invalid_request(self):
#         request_data = {}
#         request = self.factory.post('create_playlist_based_on_parameters', request_data)
#         response = EmotionFromPhotoView.as_view({'post': 'create'})(request)
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('Invalid request', response.data['message'])
#
#     def test_valid_request(self):
#         request_data = {
#             'emotion': 'happy',
#             'personalization': 'low',
#             'popularity': 'low',
#             'genres': [
#                 'genre1',
#                 'genre2',
#                 'genre3'
#             ]
#         }
#         request = self.factory.post('create_playlist_based_on_parameters', request_data)
#         response = PlaylistBasedOnParametersView.as_view({'post': 'create'})(request)
#         print(response.data)
#         self.assertEqual(response.status_code, 200)
