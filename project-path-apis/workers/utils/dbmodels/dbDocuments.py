import enum
from utils.dbmodels.modelsbase import BaseModel, db
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

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
    embedding = db.Column(Vector(),nullable=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_projects.id"), nullable=False, index=True)
    added_by = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_users.id"), nullable=False, index=True)
    

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


class User(BaseModel):
    __tablename__ = "tbl_users"
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    google_id = db.Column(db.String(120), unique=True)
    status = db.Column(db.Integer())

class Projects(BaseModel):
    __tablename__ = "tbl_projects"
    project_name = db.Column(db.String(), nullable=False)
    project_description = db.Column(db.String(), nullable=False)
    project_start_date = db.Column(db.BigInteger(), nullable=False)
    project_end_date = db.Column(db.BigInteger(), nullable=False)
    org_id = db.Column(UUID(as_uuid=True), nullable=False, index=True)
    project_status = db.Column(db.Integer(), nullable=False,default=1)

class DocumentEmbedings(BaseModel):
    __tablename__ = "tbl_document_embedings"
    document_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_project_documents.id"), nullable=False, index=True)
    chunk_text = db.Column(db.Text(), unique=False, nullable=False)
    embedding = db.Column(Vector(),nullable=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_projects.id"), nullable=False, index=True)