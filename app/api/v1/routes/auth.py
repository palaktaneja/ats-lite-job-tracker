from flask import Blueprint, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt
from app.core.redis_client import get_redis_client
from app.core.rate_limiter import rate_limit
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    redis_client = get_redis_client()

    redis_client.setex(jti, 3600, "revoked")  # expire after 1 hour

    return {"message": "Successfully logged out"}

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {"error": "Missing fields"}, 400

    register_user(name, email, password)

    return {"message": "User registered successfully"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    rate_limit(
        key=f"login:{email}",
        limit=5,
        window_seconds=60
    )

    tokens = login_user(email, password)

    if not tokens:
        return {"error": "Invalid email or password"}, 401

    return tokens, 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)

    return {"access_token": new_access_token}, 200