from app import db


class TripStop(db.Model):
    __tablename__ = 'trips_stops'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    address = db.Column(db.String(255), nullable=True)
    is_flight = db.Column(db.Boolean, nullable=True, default=False)
    airport = db.Column(db.String(255), nullable=True)
    flight_code = db.Column(db.String(6), nullable=True)
    stop_datetime = db.Column(db.DateTime, nullable=True)
    stop_pax = db.Column(db.Integer, nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())
