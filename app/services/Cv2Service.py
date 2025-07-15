import cv2

class Cv2Service:
    def __init__(self):
        self.haarcascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recover_face(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.haarcascade.detectMultiScale(frame, scaleFactor=1.099, minNeighbors=4, minSize=(20, 20))
        return faces

    def face_blur(self, frame, positions):
        original_frame = frame
        for x, y, w, h in positions:
            frame_blur = frame[y:y+h, x:x+w]
            frame_blur = cv2.GaussianBlur(frame_blur, (51,51), 0)
            original_frame[y:y+h, x:x+w] = frame_blur
        return original_frame