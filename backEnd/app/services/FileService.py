import os
import tempfile


class FileService:
    def __init__(self):
        self.temp_videos = []

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
