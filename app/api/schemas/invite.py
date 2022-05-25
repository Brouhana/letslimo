from app import ma, db
from app.models.invoices import Invoice
from app.api.schemas.trips import TripSchema
from app.api.schemas.contacts_customer import ContactsCustomerSchema
from marshmallow import fields


class InviteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        sqla_session = db.session
        load_instance = True
        include_fk = True

    company_id = fields.Integer(required=True)
    contacts_customer = fields.Nested(
        ContactsCustomerSchema,
        exclude=('created_at',
                 'updated_at', 'company_id'),
        required=True)
    trip = fields.Nested(
        TripSchema,
        exclude=('created_at',
                 'updated_at', 'company_id'),
        required=True)
    amount_due = fields.Float(required=True)
    message = fields.String(required=False)
    due_on = fields.DateTime(required=True)
    is_active = fields.Boolean(required=False, default=True)
