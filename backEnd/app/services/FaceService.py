import cv2

from backEnd.app.model.TypeAlgorithm import TypeAlgorithm


class FaceService:
    def __init__(self, cv2_service, file_service):
        self.cv2_service = cv2_service
        self.file_service = file_service

    def blur_video(self, video_bytes, algorithm=TypeAlgorithm.HAARCASCADE):
        capture = cv2.VideoCapture(self.file_service.create_temp_file(suffix=".mp4", video_bytes=video_bytes))
        frame_blurred = []
        fps = int(capture.get(cv2.CAP_PROP_FPS))
        self.read_video(capture, frame_blurred, algorithm)

        height, width, layers = frame_blurred[0].shape
        video_path = self.file_service.create_temp_file(suffix=".mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        for frame in frame_blurred:
            out.write(frame)
        out.release()

        with open(video_path, 'rb') as f:
            video_result_bytes = f.read()

        self.file_service.clean_temp_videos()
        return video_result_bytes

    def read_video(self, capture, frame_blurred, algorithm):
        width_original = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height_original = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while True:
            ok, frame = capture.read()

            if not ok:
                break
            frame = cv2.resize(frame, (640, 360))
            faces_positions = None
            if algorithm == TypeAlgorithm.HAARCASCADE:
                faces_positions = self.cv2_service.recover_face_cv2(frame)

            elif algorithm == TypeAlgorithm.DLIB:
                faces_positions = self.cv2_service.recover_face_dlib(frame)

            faces_blur = self.cv2_service.face_blur_cv2(frame, faces_positions, algorithm=algorithm)
            faces_blur = cv2.resize(faces_blur, (width_original, height_original))
            frame_blurred.append(faces_blur)

        capture.release()
