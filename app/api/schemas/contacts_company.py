from app import ma, db
from app.models.contacts_companies import ContactsCompany
from marshmallow import fields, validate


class ContactsCompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContactsCompany
        sqla_session = db.session
        load_instance = True

    company_id = fields.Integer(required=True)
    name = fields.String(
        required=True, validate=validate.Length(min=1, max=255))
    email = fields.String(required=False)
    phone = fields.String(
        required=False, validate=validate.Length(max=20))
    address = fields.String(
        required=False, validate=validate.Length(max=255))
    website_url = fields.String(is_required=False)
    description = fields.String(required=False)
    is_favorite = fields.Boolean(required=False)
    is_active = fields.Boolean(required=False)
