import cv2


class FaceService:
    def __init__(self, cv2_service):
        self.cv2_service = cv2_service

    def blur_video(self, video_bytes):
        capture = cv2.VideoCapture(video_bytes)
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            frame = cv2.resize(frame, (640, 400))
            faces_positions = self.cv2_service.recover_face(frame)
            frame_blurred = self.cv2_service.face_blur(frame, faces_positions)
