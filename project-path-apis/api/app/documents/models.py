
from app.utilities.models import BaseModel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

db = SQLAlchemy()


class ProjectDocuments(BaseModel):
    """Organization details.
        Organization can have multiple data, like logo URL, Payment.
    """
    __tablename__ = "tbl_project_documents"
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_organizations.id"), nullable=False, index=True)
    upload_file_name = db.Column(db.String(), unique=False, nullable=False)
    upload_file_type = db.Column(db.String(), unique=False, nullable=False)
    file_password = db.Column(db.String(), unique=False, nullable=True)
    upload_file_raw_url = db.Column(db.Text(), unique=False, nullable=True)
    extracted_content_url = db.Column(db.Text(), unique=False, nullable=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_projects.id"), nullable=False, index=True)
    added_by = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_users.id"), nullable=False, index=True)
    

class DocumentEmbedings(BaseModel):
    __tablename__ = "tbl_document_embedings"
    document_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_project_documents.id"), nullable=False, index=True)
    chunk_text = db.Column(db.Text(), unique=False, nullable=False)
    embedding = db.Column(Vector(),nullable=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_projects.id"), nullable=False, index=True)