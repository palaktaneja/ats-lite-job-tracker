from flask import Flask

from app.core.config import Config
from app.core.extensions import db, jwt

from app.api.v1.routes.jobs import job_bp
from app.api.v1.routes.auth import auth_bp

from app.core.exceptions import AppException
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        response = {
            "error": error.message
        }
        return jsonify(response), error.status_code

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(job_bp)
    app.register_blueprint(auth_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return {"message": "ATS-Lite API is running"}

    return app