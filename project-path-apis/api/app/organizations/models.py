import enum
from app.utilities.models import BaseModel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class CategoryType(enum.Enum):
    Individual = "Individual"
    Organization = "Organization"

    def __str__(self) -> str:
        return self.value


class Organization(BaseModel):
    """Organization details.

    Though organizations can have the same name,
    A single user cannot register two organizations with the same name.
    """
    __tablename__ = "tbl_organizations"
    name = db.Column(db.String(), unique=False, nullable=False, index=True)
    location = db.Column(db.String(), unique=False, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False)
    registered_by = db.Column(
        UUID(as_uuid=True), db.ForeignKey("tbl_users.id"), nullable=False, index=True
    )
    org_type = db.Column(db.Enum(CategoryType), nullable=True)
    __table_args__ = (
        db.UniqueConstraint("name", "registered_by", name="user_reg_org"),)
    usernames = relationship("User",  uselist=False)

    @hybrid_property
    def registered_by_name(self):
        return self.usernames.first_name

class OrgUser(BaseModel):
    """Organizations users belong to."""
    __tablename__ = "tbl_org_users"
    org_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("tbl_organizations.id"),
        nullable=False,
        index=True,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("tbl_users.id"), nullable=False, index=True
    )
    user_status = db.Column(db.Integer(), nullable=False)
    user_type = db.Column(db.String(), nullable=True,default='STAFF')
    __table_args__ = (db.UniqueConstraint("org_id", "user_id", name="user_org"),)
    users = relationship("User", uselist=False)

    @hybrid_property
    def user_names(self):
        return f"{self.users.first_name} {self.users.last_name}"

    @classmethod
    def find_user_orgs(cls, user_id: str):
        return cls.query.filter_by(user_id=user_id).all()