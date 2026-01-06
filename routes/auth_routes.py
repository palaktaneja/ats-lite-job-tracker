from flask import Blueprint, request 
from extensions import db
from models.user import User

auth_bp= Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods="POST")
def register():
    data = request.get_json()

    name= data.get("name")
    email= data.get("email")
    password= data.get("password")

    if not name or not email or not password:
        return {"error": "Name, email and password are required"}, 400
    
    if User.query.filter_by(email=email).first():
        return {"error": "User already exists"}, 400
    
    user= User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data= request.get_json()
    email= data.get("email")
    password= data.get("password")

    user= User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid email or password"}, 401

    return {"message": "Login successful", "user_id": user.id}, 200
