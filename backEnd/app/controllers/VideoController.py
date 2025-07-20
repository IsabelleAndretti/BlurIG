from flask import Blueprint, request, Response

from backEnd.app.error.Error_model import Error_model
from backEnd.app.model.TypeAlgorithm import TypeAlgorithm
from backEnd.app.services.CvService import CvService
from backEnd.app.services.FaceService import FaceService
from backEnd.app.services.FileService import FileService

video_bp = Blueprint('video_bp', __name__)
cv2_service = CvService()
file_service = FileService()
face_service = FaceService(cv2_service, file_service)


@video_bp.route("/blur", methods=["POST"])
def blur_video():
    if 'file' not in request.files:
        return Error_model("Argument 'file' not found.", 400).show()

    video = request.files['file']

    if not video.mimetype.startswith('video/'):
        return Error_model("The uploaded file is not a valid video.", 400).show()

    video_bytes = video.read()
    video_bytes_with_blur = face_service.blur_video(video_bytes, algorithm=TypeAlgorithm(request.form['algorithm']))
    return Response(video_bytes_with_blur, mimetype="video/mp4")
