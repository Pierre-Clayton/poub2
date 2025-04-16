from app.psychometrics.models import PsychometricScores
from app.utilities.models import ma
from marshmallow import fields, Schema


class PsychometricScoresSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PsychometricScores
        fields = ("id", "user_id", "mbti_scores", "mbti_type", "bfi_scores", "bfi_type")
        include_fk = True


class PsychoResponsesSchema(Schema):
    question = fields.String(required=True)
    response = fields.String(required=True)
    

class PsychometricPostSchema(Schema):
    user_id = fields.UUID(required=True)
    test_type = fields.String(required=True)
    questions = fields.Nested(PsychoResponsesSchema, many=True)

