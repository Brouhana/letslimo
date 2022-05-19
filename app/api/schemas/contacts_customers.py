from app import db
from app import ma, db
from app.models.contacts_customers import ContactsCustomer
from marshmallow import fields, validate


class ContactsCustomers(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContactsCustomer
        sqla_session = db.session
        load_instance = True

    first_name = fields.String(
        required=True, validate=validate.Length(min=1, max=90))
    last_name = fields.String(
        required=True, validate=validate.Length(min=1, max=90))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    contacts_company_id = fields.Integer(required=True)
    home_address = fields.String(
        required=False, validate=validate.Length(max=255))
    work_address = fields.String(
        required=False, validate=validate.Length(max=255))
    work_position = fields.String(
        required=False, validate=validate.Length(max=255))
    notes = fields.String(required=False)
    is_favorite = fields.Boolean(required=False)
    is_active = fields.Boolean(required=False)
