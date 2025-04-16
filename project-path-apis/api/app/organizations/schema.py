from app.utilities.models import ma
from marshmallow_enum import EnumField
from app.organizations.models import CategoryType
from app.organizations.models import Organization, OrgUser
from marshmallow import fields, Schema



class OrganizationSchema(ma.SQLAlchemyAutoSchema):
    org_type = EnumField(CategoryType)
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "location",
            "description",
            "registered_by",
            "org_type",
            "registered_by_name",
        )
        include_fk = True



class OrganizationPutSchema(Schema):
    name = fields.String()
    location = fields.String()
    description = fields.String()



class OrgUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrgUser
        fields = (
            "id",
            "org_id",
            "user_id",
            "user_status",
            "user_names",
            "user_type",
        )
        include_fk = True

