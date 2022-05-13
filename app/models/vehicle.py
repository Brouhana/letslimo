from app import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    # Basic vehicle information
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    pax_capacity = db.Column(db.Integer, nullable=False)
    license_plate_number = db.Column(db.String(12), nullable=False)
    exterior_color = db.Column(db.String(120), nullable=True)
    vin_number = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    # General vehicle features
    has_air_conditioning = db.Column(db.Boolean, default=False)
    has_dance_pole = db.Column(db.Boolean, default=False)
    has_luggage_space = db.Column(db.Boolean, default=False)
    has_tables = db.Column(db.Boolean, default=False)
    has_onboard_bathroom = db.Column(db.Boolean, default=False)
    has_onboard_bar = db.Column(db.Boolean, default=False)
    has_refrigerator = db.Column(db.Boolean, default=False)
    has_trash_can = db.Column(db.Boolean, default=False)
    has_ice_chest = db.Column(db.Boolean, default=False)
    has_wheelchair_accessibility = db.Column(db.Boolean, default=False)
    # Vehicle media features
    has_aux = db.Column(db.Boolean, default=False)
    has_bluetooth = db.Column(db.Boolean, default=False)
    has_dvd_player = db.Column(db.Boolean, default=False)
    has_karaoke = db.Column(db.Boolean, default=False)
    has_usb = db.Column(db.Boolean, default=False)
    has_power_outlets = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    has_tv = db.Column(db.Boolean, default=False)
    has_gaming_console = db.Column(db.Boolean, default=False)
    # Vehicle policies
    is_alcohol_allowed = db.Column(db.Boolean, default=False)
    is_smoking_allowed = db.Column(db.Boolean, default=False)
    is_pets_allowed = db.Column(db.Boolean, default=False)
    is_food_allowed = db.Column(db.Boolean, default=False)
    is_children_allowed = db.Column(db.Boolean, default=False)
    # Vehicle pricing
    min_total_base_rate = db.Column(db.Integer, nullable=True)
    deadhead_rate_per_mile = db.Column(db.Integer, nullable=True)
    trip_rate_per_mile = db.Column(db.Integer, nullable=True)
    weekend_hourly_rate = db.Column(db.Integer, nullable=True)
    weekend_hourly_min = db.Column(db.Integer, nullable=True)
    weekday_hourly_rate = db.Column(db.Integer, nullable=True)
    weekday_hourly_min = db.Column(db.Integer, nullable=True)
    total_deadhead_duration = db.Column(db.Integer, nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<Vehicle %s>' % self.id
