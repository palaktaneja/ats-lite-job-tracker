from flask import Flask

from app.core.config import Config
from app.core.extensions import db, jwt, migrate

from app.api.v1.routes.jobs import job_bp
from app.api.v1.routes.auth import auth_bp

from app.core.exceptions import AppException
from flask import jsonify

from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt

from app.core.redis_client import get_redis_client


def register_jwt_callbacks(jwt):

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        redis_client = get_redis_client()

        return redis_client.exists(jti)

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
    migrate.init_app(app, db)
    register_error_handlers(app)


    # Register blueprints
    app.register_blueprint(job_bp)
    app.register_blueprint(auth_bp)

    register_jwt_callbacks(jwt)

    @app.route("/")
    def home():
        return {"message": "ATS-Lite API is running"}

    return app