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