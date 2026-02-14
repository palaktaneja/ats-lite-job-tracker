from flask import Blueprint, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


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