from flask import Blueprint, request, Response

from app.error.Error_model import Error_model
from app.services.CvService import CvService
from app.services.FaceService import FaceService
from app.services.FileService import FileService

video_bp = Blueprint('video_bp', __name__)
cv2_service = CvService()
file_service = FileService()
face_service = FaceService(cv2_service, file_service)


@video_bp.route("/blur", methods=["POST"])
def blur_video():
    if 'file' not in request.files:
        return Error_model("file not found.", 400).show()
    video = request.files['file']
    video_bytes = video.read()
    video_bytes_with_blur = face_service.blur_video(video_bytes, algorithm="dlib")
    return Response(video_bytes_with_blur, mimetype="video/mp4")
