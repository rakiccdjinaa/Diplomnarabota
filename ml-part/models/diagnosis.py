from models.user import db
from datetime import datetime


class Diagnosis(db.Model):

    __tablename__ = "diagnoses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    probability = db.Column(
        db.Float,
        nullable=False
    )

    prediction = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
