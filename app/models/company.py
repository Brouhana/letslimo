from app import db


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)

    # Basic company information
    company_name = db.Column(db.String(255), nullable=False)
    company_address = db.Column(db.String(255), nullable=False)
    company_website_url = db.Column(db.String(255), nullable=False)
    company_general_email = db.Column(db.String(120), nullable=False)
    company_booking_email = db.Column(db.String(120), nullable=False)
    company_phone = db.Column(db.String(120), nullable=False)

    # Stripe connected account
    stripe_account = db.Column(db.String(255), nullable=True)

    enabled_auto_invoice = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<Company %s>' % self.id
