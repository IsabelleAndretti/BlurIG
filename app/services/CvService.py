import cv2
import dlib


class CvService:
    def __init__(self):
        self.haarcascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.dlib_frontal_face = dlib.get_frontal_face_detector()

    def recover_face_cv2(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.haarcascade.detectMultiScale(frame, scaleFactor=1.099, minNeighbors=4, minSize=(20, 20))
        return faces

    def face_blur_cv2(self, frame, positions, algorithm="haarcascade"):
        original_frame = frame
        for x, y, w, h in positions:
            if algorithm == "haarcascade":
                h = y + h
                w = x + w
            elif algorithm == "dlib":
                h = h
                w = w

            frame_blur = frame[y:h, x:w]
            frame_blur = cv2.GaussianBlur(frame_blur, (51, 51), 0)
            original_frame[y:h, x:w] = frame_blur
        return original_frame

    def recover_face_dlib(self, frame):
        faces_detected = self.dlib_frontal_face(frame, 2)
        return [[face.left(), face.top(), face.right(), face.bottom()] for face in faces_detected]
