from app.core.extensions import db
from app.models.user import User
from app.core.exceptions import ConflictException


def register_user(name, email, password):

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        raise ConflictException("User already exists")

    user = User(name=name, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user