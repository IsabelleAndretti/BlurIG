import os
import tempfile

import cv2


class FaceService:
    def __init__(self, cv2_service):
        self.cv2_service = cv2_service
        self.temp_videos = []

    def blur_video(self, video_bytes):
        capture = cv2.VideoCapture(self.create_temp_file(suffix=".mp4", video_bytes=video_bytes))
        frame_blurred = []
        width_original = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height_original = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            frame = cv2.resize(frame, (640, 360))
            faces_positions = self.cv2_service.recover_face(frame)
            faces_blur = self.cv2_service.face_blur(frame, faces_positions)
            faces_blur = cv2.resize(faces_blur, (width_original, height_original))
            frame_blurred.append(faces_blur)

        capture.release()
        height, width, layers = frame_blurred[0].shape
        video_path = self.create_temp_file(suffix=".mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        for frame in frame_blurred:
            out.write(frame)
        out.release()

        with open(video_path, 'rb') as f:
            video_result_bytes = f.read()

        self.clean_temp_videos()
        return video_result_bytes

    def create_temp_file(self, suffix, video_bytes=None):
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_video_file:
            if video_bytes is not None:
                temp_video_file.write(video_bytes)
            temp_video_path = temp_video_file.name
            self.temp_videos.append(temp_video_path)
            return temp_video_path

    def clean_temp_videos(self):
        for video in self.temp_videos:
            os.remove(video)
        self.temp_videos.clear()
