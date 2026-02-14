from flask import Flask

from app.core.config import Config
from app.core.extensions import db, jwt

from app.api.v1.routes.jobs import job_bp
from app.api.v1.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

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