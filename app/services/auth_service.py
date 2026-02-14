from flask_jwt_extended import create_access_token, create_refresh_token
from app.core.extensions import db
from app.models.user import User
from app.core.exceptions import ConflictException


def register_user(name: str, email: str, password: str):
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        raise ConflictException("User already exists")

    role = "ADMIN" if email.endswith("@admin.com") else "USER"

    user = User(
        name=name,
        email=email,
        role=role
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user


def login_user(email: str, password: str):
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return None

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }