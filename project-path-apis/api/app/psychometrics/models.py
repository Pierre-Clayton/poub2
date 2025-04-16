import enum

from sqlalchemy import null
from app.utilities.models import BaseModel, db
from sqlalchemy.dialects.postgresql import ARRAY, UUID



class PsychometricScores(BaseModel):
    __tablename__ = "tbl_personality_scores"
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("tbl_users.id"), nullable=False, index=True)
    mbti_scores= db.Column(db.String(),nullable=True)
    mbti_type = db.Column(db.String(),nullable=True)
    bfi_scores = db.Column(db.String(),nullable=True)
    bfi_type = db.Column(db.String(),nullable=True)
    


