from flask import Blueprint

video_bp = Blueprint('user_bp', __name__)

@video_bp.route("/users", methods=["GET"])
def get_test():
    return "seilaaaa"