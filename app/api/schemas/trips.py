from app import ma, db
from app.models.trips import Trip
from app.api.schemas.user import UserSchema
from app.api.schemas.contacts.contacts_customer import ContactsCustomerSchema
from marshmallow import fields, validate


class TripSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trip
        sqla_session = db.session
        load_instance = True
        include_fk = True

    company_id = fields.Integer(required=True)
    stops = fields.List(fields.Dict(), required=False)
    contacts_customer = fields.Nested(
        ContactsCustomerSchema,
        exclude=('notes', 'created_at', 'home_address',
                 'updated_at', 'company_id'),
        required=True)
    driver_user = fields.Nested(UserSchema, exclude=(
        'created_on', 'is_admin', 'is_owner', 'is_member',
        'is_driver', 'last_updated', 'company_id', 'DL_expr', 'DL_number', 'DL_state'),
    )
    category = fields.String(required=True, validate=validate.Length(max=50))
    vehicle_id = fields.Integer(required=True)
    type = fields.String(required=True, validate=validate.Length(max=15))
    pu_datetime = fields.DateTime(required=False)
    pu_address = fields.String(
        required=False, validate=validate.Length(max=255))
    pu_is_flight = fields.Boolean(required=False, default=False)
    pu_arrival_airport = fields.String(
        required=False, validate=validate.Length(max=255))
    pu_flight_code = fields.String(
        required=False, validate=validate.Length(max=6))
    pu_airline = fields.String(
        required=False, validate=validate.Length(max=255))
    do_datetime = fields.DateTime(required=False)
    do_address = fields.String(
        required=False, validate=validate.Length(max=255))
    do_is_flight = fields.Boolean(required=False, default=False)
    do_departure_airport = fields.String(
        required=False, validate=validate.Length(max=255))
    do_flight_code = fields.String(
        required=False, validate=validate.Length(max=6))
    do_airline = fields.String(
        required=False, validate=validate.Length(max=255))
    pu_pax = fields.Integer(required=True)
    do_pax = fields.Integer(required=False)
    notes = fields.String(required=False)
    driver_notes = fields.String(required=False)
    status = fields.Integer(required=False)
    price_gratituity = fields.Float(required=False)
    price_tax = fields.Float(required=False)
    price_tolls = fields.Float(required=False)
    price_discount = fields.Float(required=False)
    price_other1 = fields.Float(required=False)
    price_other2 = fields.Float(required=False)
    price_other3 = fields.Float(required=False)
    price_other4 = fields.Float(required=False)
    base_rate = fields.Float(required=False)
    has_stops = fields.Boolean(required=False, default=False)
    is_active = fields.Boolean(required=False, default=True)
