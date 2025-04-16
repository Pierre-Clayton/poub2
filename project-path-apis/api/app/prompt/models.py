
from app.utilities.models import BaseModel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class RetrievalHistory(BaseModel):
    __tablename__ = "tbl_prompt_history"
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_organizations.id"), nullable=False, index=True)
    prompt_text = db.Column(db.Text(), unique=False, nullable=False)
    prompt_response = db.Column(db.Text(), unique=False, nullable=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_projects.id"), nullable=False, index=True)
    added_by = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_users.id"), nullable=False, index=True)
