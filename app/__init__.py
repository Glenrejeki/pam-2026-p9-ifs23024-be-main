from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
from app.routes.space_object_routes import space_object_bp
from app.routes.plant_routes import plant_bp
from app.routes.profile_routes import profile_bp
from app.routes.ai_routes import ai_bp
import os

def create_app():
    app = Flask(__name__)

    CORS(app,
         origins="*",
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
         )

    Base.metadata.create_all(bind=engine)

    for folder in ["uploads/plants", "uploads/space", "uploads/profile"]:
        os.makedirs(folder, exist_ok=True)

    # Serve static files dari folder uploads
    app.config["UPLOAD_FOLDER"] = "uploads"

    app.register_blueprint(space_object_bp)
    app.register_blueprint(plant_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(ai_bp)

    # Route index
    @app.route("/")
    def index():
        return "API telah berjalan! Dibuat oleh Abdullah Ubaid"

    # Serve static files
    from flask import send_from_directory

    @app.route("/static/<path:filename>")
    def static_files(filename):
        return send_from_directory("uploads", filename)

    return app