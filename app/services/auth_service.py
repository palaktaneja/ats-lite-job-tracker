from flask_jwt_extended import create_access_token, create_refresh_token
from app.core.extensions import db
from app.models.user import User
from app.core.exceptions import ConflictException
import logging

logger = logging.getLogger(__name__)


def register_user(name: str, email: str, password: str):
    logger.info(f"Attempting to register user with email: {email}")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        logger.error(f"Registration failed - User already exists: {email}", exc_info=True)
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

    logger.info(f"User registered successfully with email: {email}")

    return user


def login_user(email: str, password: str):
    logger.info(f"Login attempt for email: {email}")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        logger.warning(f"Login failed for email: {email}")
        return None

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    logger.info(f"Login successful for email: {email}")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }