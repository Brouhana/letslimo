from app import ma, db
from app.models.trips_stops import TripStop
from marshmallow import fields, validate


class TripStopSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TripStop
        sqla_session = db.session
        load_instance = True

    trip_id = fields.Integer(required=True)
    address = fields.String(
        is_required=False, validate=validate.Length(max=255))
    is_flight = fields.Boolean(required=False, default=False)
    airport = fields.String(
        is_required=False, validate=validate.Length(max=255))
    flight_code = fields.String(
        required=False, validate=validate.Length(max=6))
    stop_datetime = fields.Date(required=False)
    stop_pax = fields.Integer(required=False)
