# file: app.py
from flask import Flask
from flask_cors import CORS
from app.routes.panel_routes import panel_bp
from app.config import Config
import os


def create_app():
    """Application factory for creating Flask app instances"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://panelize-frontend.onrender.com").split(",")
    CORS(app, origins=allowed_origins)
    
    # Register blueprints
    app.register_blueprint(panel_bp, url_prefix="/api")
    
    return app


app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)


