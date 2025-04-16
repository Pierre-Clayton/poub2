import enum

from sqlalchemy import null
from app.utilities.models import BaseModel, db
from sqlalchemy.dialects.postgresql import ARRAY, UUID


class Projects(BaseModel):
    __tablename__ = "tbl_projects"
    project_name = db.Column(db.String(), nullable=False)
    project_description = db.Column(db.String(), nullable=False)
    project_start_date = db.Column(db.BigInteger(), nullable=False)
    project_end_date = db.Column(db.BigInteger(), nullable=False)
    org_id = db.Column(UUID(as_uuid=True), nullable=False, index=True)
    project_status = db.Column(db.Integer(), nullable=False,default=1)


