from app import db


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    # Basic company information
    company_name = db.Column(db.String(255), nullable=False)
    company_address = db.Column(db.String(255), nullable=False)
    company_website_url = db.Column(db.String(255), nullable=False)
    company_general_email = db.Column(db.String(120), nullable=False)
    company_booking_email = db.Column(db.String(120), nullable=False)
    company_phone = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    user_operators = db.relationship(
        'OperatorUser', backref='company', lazy=True)
    vehicles = db.relationship('Vehicle', backref='company', lazy=True)
    user_drivers = db.relationship('DriverUser', backref='company', lazy=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<Company %s>' % self.id
