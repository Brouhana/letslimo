from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSON
from uuid import uuid4


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, unique=True)

    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    company = db.relationship('Company', backref='vehicles', lazy=True)

    name = db.Column(db.String(120), nullable=False)
    vehicle_type = db.Column(JSON, nullable=False)
    pax_capacity = db.Column(db.Integer, nullable=False)
    features = db.Column(JSON, nullable=True)
    description = db.Column(db.Text(), nullable=True)
    license_plate_number = db.Column(db.String(12), nullable=True)
    exterior_color = db.Column(db.String(120), nullable=True)
    vin_number = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    features = db.Column(JSON, nullable=True)

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
