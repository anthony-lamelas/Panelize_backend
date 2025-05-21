# file: app.py
from flask import Flask
from app.routes.panel_routes import panel_bp  
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.register_blueprint(panel_bp, url_prefix="/api")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


