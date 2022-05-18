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

    has_air_conditioning = fields.Boolean(required=False)
    has_dance_pole = fields.Boolean(required=False)
    has_luggage_space = fields.Boolean(required=False)
    has_tables = fields.Boolean(required=False)
    has_onboard_bathroom = fields.Boolean(required=False)
    has_onboard_bar = fields.Boolean(required=False)
    has_refrigerator = fields.Boolean(required=False)
    has_trash_can = fields.Boolean(required=False)
    has_ice_chest = fields.Boolean(required=False)
    has_wheelchair_accessibility = fields.Boolean(required=False)

    has_aux = fields.Boolean(required=False)
    has_bluetooth = fields.Boolean(required=False)
    has_dvd_player = fields.Boolean(required=False)
    has_karaoke = fields.Boolean(required=False)
    has_usb = fields.Boolean(required=False)
    has_power_outlets = fields.Boolean(required=False)
    has_wifi = fields.Boolean(required=False)
    has_tv = fields.Boolean(required=False)
    has_gaming_console = fields.Boolean(required=False)

    is_alcohol_allowed = fields.Boolean(required=False)
    is_smoking_allowed = fields.Boolean(required=False)
    is_pets_allowed = fields.Boolean(required=False)
    is_food_allowed = fields.Boolean(required=False)
    is_children_allowed = fields.Boolean(required=False)

    min_total_base_rate = fields.Integer(required=False)
    deadhead_rate_per_mile = fields.Integer(required=False)
    trip_rate_per_mile = fields.Integer(required=False)
    weekend_hourly_rate = fields.Integer(required=False)
    weekend_hourly_min = fields.Integer(required=False)
    weekday_hourly_rate = fields.Integer(required=False)
    weekday_hourly_min = fields.Integer(required=False)
    total_deadhead_duration = fields.Integer(required=False)
