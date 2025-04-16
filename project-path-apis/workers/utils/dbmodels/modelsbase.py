from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

db = SQLAlchemy()

class BaseModel(db.Model):
    """Defines base fields and common helper methods."""

    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
    )


    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )

    