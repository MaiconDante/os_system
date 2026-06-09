from app import db
from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# User model
class User(
    db.Model,
    UserMixin
):
    # Table name
    __tablename__ = "users"

    # Columns
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # User's name
    name = db.Column(
        db.String(120),
        nullable=False
    )

    # User's email
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # User's password hash
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )
    