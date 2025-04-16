from app.documents.models import ProjectDocuments
from app.utilities.models import ma
from marshmallow import fields, Schema


class ProjectDocumentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProjectDocuments
        fields = ("id", "upload_file_name", "upload_file_type", "upload_file_extract_url", "org_id","upload_file_raw_url","project_id","added_by")
        load_only = ("file_password",)
        include_fk = True

class UploadPostSchema(Schema):
    uploaded_file = fields.Field(required=True)
    file_password = fields.String(required=False)
    project_id = fields.UUID()
    org_id = fields.UUID()

