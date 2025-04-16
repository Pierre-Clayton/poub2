from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

db = SQLAlchemy()
ma = Marshmallow()


class BaseModel(db.Model):
    """Defines base fields and common helper methods."""

    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
        onupdate=func.current_timestamp(),)


    @classmethod
    def save_to_db(cls, data: dict) -> None:
        new_object = cls(**data)
        db.session.add(new_object)
        db.session.commit()
        return new_object

    @staticmethod
    def update_record():
        db.session.commit()
