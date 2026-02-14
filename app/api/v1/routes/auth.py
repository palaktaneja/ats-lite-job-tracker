from flask import Blueprint, request 
from app.core.extensions import db
from app.models.user import User
from app.core.exceptions import ConflictException
from app.services.auth_service import register_user
from flask_jwt_extended import create_access_token

auth_bp= Blueprint("auth", __name__, url_prefix="/auth")

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
    data= request.get_json()
    email= data.get("email")
    password= data.get("password")

    user= User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid email or password"}, 401
    
    access_token= create_access_token(identity=str(user.id))

    return {
        "message": "Login successful",
        "access_token": access_token
    }, 200
