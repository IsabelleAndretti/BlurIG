from flask import Flask
from flask_cors import CORS
from backEnd.app.controllers.VideoController import video_bp

def create_app():
    app = Flask(__name__)
    CORS(app, origins = ["http://localhost:5173"])
    app.register_blueprint(video_bp)
    return app