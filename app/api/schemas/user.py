from app import ma, db
from app.models.user import User
from marshmallow import fields, validate


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('password',)
        sqla_session = db.session
        load_instance = True

    company_id = fields.Integer(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    first_name = fields.String(
        required=True, validate=validate.Length(min=2, max=50))
    last_name = fields.String(
        required=True, validate=validate.Length(min=2, max=50))
    phone = fields.String(
        required=True, validate=validate.Length(max=20))
    address = fields.String(required=False, validate=validate.Length(max=255))
    DL_number = fields.String(
        required=False, validate=validate.Length(max=50))
    DL_state = fields.String(
        required=False, validate=validate.Length(min=2, max=2))
    DL_expr = fields.Date(required=False)
    notes = fields.String(required=False)
    is_active = fields.Boolean(required=False)
    is_owner = fields.Boolean(required=False)
    is_admin = fields.Boolean(required=False)
    is_member = fields.Boolean(required=False)
    is_driver = fields.Boolean(required=False)
