from app.prompt.models import RetrievalHistory
from app.utilities.models import ma
from marshmallow import fields, Schema


class RetrievalHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RetrievalHistory
        fields = ("id", "org_id", "prompt_text", "prompt_response", "project_id","added_by","created_at")
        include_fk = True

class RetrievalSchema(Schema):
    org_id = fields.UUID(required=True)
    project_id = fields.UUID(required=True)
    prompt_text = fields.String(required=True)

