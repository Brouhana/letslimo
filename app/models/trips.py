from app import db


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    company = db.relationship(
        'Company', backref='trips', lazy=True)
    contacts_customer_id = db.Column(db.Integer, db.ForeignKey(
        'contacts_customers.id'), nullable=False)
    contacts_customer = db.relationship(
        'ContactsCustomer', backref='trips', lazy=True)
    category = db.Column(db.String(50), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey(
        'vehicles.id'), nullable=False)
    vehicle = db.relationship(
        'Vehicle', backref='trips', lazy=True)
    type = db.Column(db.String(15), nullable=False)
    pu_datetime = db.Column(db.DateTime, nullable=False)
    pu_address = db.Column(db.String(255), nullable=True)
    pu_is_flight = db.Column(db.Boolean, nullable=True, default=False)
    pu_arrival_airport = db.Column(db.String(255), nullable=True)
    pu_flight_code = db.Column(db.String(6), nullable=True)
    pu_airline = db.Column(db.String(255), nullable=True)
    do_datetime = db.Column(db.DateTime, nullable=True)
    do_address = db.Column(db.String(255), nullable=True)
    do_is_flight = db.Column(db.Boolean, nullable=True, default=False)
    do_departure_airport = db.Column(db.String(255), nullable=True)
    do_flight_code = db.Column(db.String(6), nullable=True)
    do_airline = db.Column(db.String(255), nullable=True)
    pu_pax = db.Column(db.Integer, nullable=False)
    do_pax = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    driver_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, nullable=False)
    price_gratituity = db.Column(db.Float, nullable=True)
    price_tax = db.Column(db.Float, nullable=True)
    price_tolls = db.Column(db.Float, nullable=True)
    price_discount = db.Column(db.Float, nullable=True)
    price_other1 = db.Column(db.Float, nullable=True)
    price_other2 = db.Column(db.Float, nullable=True)
    price_other3 = db.Column(db.Float, nullable=True)
    price_other4 = db.Column(db.Float, nullable=True)
    base_rate = db.Column(db.Float, nullable=True)
    has_stops = db.Column(db.Boolean, nullable=True, default=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())
