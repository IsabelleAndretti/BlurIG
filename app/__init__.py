from flask import Flask

def create_app():
    app = Flask(__name__)
    from app.controllers.VideoController import video_bp
    app.register_blueprint(video_bp)
    return app