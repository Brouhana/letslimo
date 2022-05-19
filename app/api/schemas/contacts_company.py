from app import ma, db
from app.models.contacts_companies import ContactsCompany
from marshmallow import fields, validate


class ContactsCompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContactsCompany
        sqla_session = db.session
        load_instance = True

    name = fields.String(
        required=True, validate=validate.Length(min=1, max=255))
    email = fields.Email(required=False)
    phone = fields.String(
        required=False, validate=validate.Length(max=20))
    address = fields.String(
        is_required=False, validate=validate.Length(max=255))
    website_url = fields.URL(is_required=False)
    description = fields.String(required=False)
    is_favorite = fields.Boolean(required=False)
