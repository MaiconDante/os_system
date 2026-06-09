from app import db
from datetime import datetime

class OrderService(db.Model):

    __tablename__ = "order_services"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    equipment = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    technical_notes = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Aberto"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    client_id = db.Column(
        db.Integer,
        db.ForeignKey("clients.id"),
        nullable=False
    )
