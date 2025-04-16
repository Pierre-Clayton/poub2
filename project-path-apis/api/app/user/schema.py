
from flask_marshmallow import Schema
from app.user.models import User
from app.utilities.models import ma
from marshmallow import fields, Schema


class UserSchema(ma.SQLAlchemyAutoSchema):
    model = User
    class Meta:
        fields = ('id', 'username', 'email')
        load_only = ('password', )

class UserRegSchema(Schema):
    username = fields.String()
    password = fields.String(required=False)
    email = fields.String()
    google_id_token = fields.String(required=False)

class UserPUTSchema(Schema):
    status = fields.Integer()
    email = fields.String()

class LoginWebInputSchema(Schema):
    password = fields.String(required=False)
    email = fields.String()
    google_id_token = fields.String(required=False)

