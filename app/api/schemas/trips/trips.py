from app import ma, db
from app.models.trips import Trip
from marshmallow import fields, validate


class TripSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trip
        sqla_session = db.session
        load_instance = True

    company_id = fields.Integer(required=True)
    contacts_customer_id = fields.Integer(required=True)
    category = fields.String(required=True, validate=validate.Length(max=50))
    vehicle_id = fields.Integer(required=True)
    type = fields.String(required=True, validate=validate.Length(max=15))
    pu_datetime = fields.Date(required=False)
    pu_address = fields.String(
        required=False, validate=validate.Length(max=255))
    pu_is_flight = fields.Boolean(required=False, default=False)
    pu_arrival_airport = fields.String(
        required=False, validate=validate.Length(max=255))
    pu_flight_code = fields.String(
        required=False, validate=validate.Length(max=6))
    pu_airline = fields.String(
        required=False, validate=validate.Length(max=255))
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
