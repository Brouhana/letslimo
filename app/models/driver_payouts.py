from app import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class DriverPayout(db.Model):
    __tablename__ = 'driver_payouts'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    company = db.relationship(
        'Company', backref='driver_payouts', lazy=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', backref='driver_payouts', lazy=True)
    driver_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=True)
    driver = db.relationship('User', backref='driver_payouts', lazy=True)
    flat_rate = db.Column(db.Float, nullable=True)
    hourly_rate = db.Column(db.Float, nullable=True)
    hours = db.Column(db.Float, nullable=True)
    gratuity = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<DriverPayout %s>' % self.id
