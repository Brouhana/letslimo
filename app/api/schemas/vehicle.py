from app import ma, db
from app.models.vehicle import Vehicle
from marshmallow import fields, validate


class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        sqla_session = db.session
        load_instance = True

    company_id = fields.Integer(required=True)
    name = fields.String(required=True)
    vehicle_type = fields.Raw(required=True)
    pax_capacity = fields.Integer(
        required=True, validate=validate.Range(min=1))
    license_plate_number = fields.String(required=True)

    description = fields.String(
        required=False, validate=validate.Length(max=120))
    exterior_color = fields.String(
        required=False, validate=validate.Length(max=120))
    vin_number = fields.String(
        required=False, validate=validate.Length(max=20))
    is_active = fields.Boolean(required=False)

    features = fields.List(fields.Dict(), required=False)

    min_total_base_rate = fields.Integer(required=False)
    deadhead_rate_per_mile = fields.Integer(required=False)
    trip_rate_per_mile = fields.Integer(required=False)
    weekend_hourly_rate = fields.Integer(required=False)
    weekend_hourly_min = fields.Integer(required=False)
    weekday_hourly_rate = fields.Integer(required=False)
    weekday_hourly_min = fields.Integer(required=False)
    total_deadhead_duration = fields.Integer(required=False)
