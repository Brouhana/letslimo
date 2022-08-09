from app import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, unique=True)

    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    company = db.relationship(
        'Company', backref='trips', lazy=True)

    driver_user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=True)
    driver_user = db.relationship(
        'User', backref='trips', lazy=True)

    contacts_customer_id = db.Column(db.Integer, db.ForeignKey(
        'contacts_customers.id'), nullable=False)
    contacts_customer = db.relationship(
        'ContactsCustomer', backref='trips', lazy=True)

    vehicle_id = db.Column(db.Integer, db.ForeignKey(
        'vehicles.id'), nullable=False)
    vehicle = db.relationship(
        'Vehicle', backref='trips', lazy=True)

    returntrip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    returntrip = db.relationship(
        'Trip', backref='trips', remote_side="Trip.id")

    tripgroup_id = db.Column(db.Integer, db.ForeignKey(
        'trip_groups.id'), nullable=True)
    tripgroup = db.relationship('TripGroup', backref='trips', lazy=True)

    is_quote = db.Column(db.Boolean, nullable=True, default=False)

    trip_code_sub = db.Column(
        db.String(10), nullable=False)
    type = db.Column(JSONB, nullable=False)
    pu_datetime = db.Column(db.DateTime, nullable=False)
    pu_address = db.Column(db.String(255), nullable=True)
    pu_is_flight = db.Column(db.Boolean, nullable=True, default=False)
    pu_arrival_airport = db.Column(JSONB, nullable=True)
    pu_flight_code = db.Column(db.String(6), nullable=True)
    pu_airline = db.Column(JSONB, nullable=True)
    do_datetime = db.Column(db.DateTime, nullable=True)
    do_address = db.Column(db.String(255), nullable=True)
    do_is_flight = db.Column(db.Boolean, nullable=True, default=False)
    do_departure_airport = db.Column(JSONB, nullable=True)
    do_flight_code = db.Column(db.String(6), nullable=True)
    do_airline = db.Column(JSONB, nullable=True)
    pu_pax = db.Column(db.Integer, nullable=False)
    do_pax = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    driver_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, nullable=True, default=0)
    price_gratuity = db.Column(JSONB, nullable=True)
    price_tax = db.Column(JSONB, nullable=True)
    price_tolls = db.Column(JSONB, nullable=True)
    price_discounts = db.Column(JSONB, nullable=True)
    price_other1 = db.Column(JSONB, nullable=True)
    price_other2 = db.Column(JSONB, nullable=True)
    price_other3 = db.Column(JSONB, nullable=True)
    price_other4 = db.Column(JSONB, nullable=True)
    price_base_rate = db.Column(JSONB, nullable=True)
    stops = db.Column(JSONB, nullable=True)
    passenger = db.Column(JSONB, nullable=True)
    is_active = db.Column(db.Boolean, nullable=True, default=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<Trip %s>' % self.id
