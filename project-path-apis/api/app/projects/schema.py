from app.projects.models import Projects
from app.utilities.models import ma
from marshmallow import fields, Schema


class ProjectsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Projects
        fields = ("id", "project_name", "project_description", "project_start_date", "org_id","project_end_date","project_status")
        include_fk = True

