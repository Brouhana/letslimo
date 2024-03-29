from app import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class ContactsCustomer(db.Model):
    __tablename__ = 'contacts_customers'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, unique=True)

    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    company = db.relationship(
        'Company', backref='contacts_customers', lazy=True)

    first_name = db.Column(db.String(90), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    full_name = db.Column(db.String(180), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(120), nullable=False)

    contacts_company_id = db.Column(db.Integer, db.ForeignKey(
        'contacts_companies.id'), nullable=True)
    contacts_company = db.relationship(
        'ContactsCompany', backref='contacts_customers', lazy=True)

    home_address = db.Column(db.String(255), nullable=True)
    work_address = db.Column(db.String(255), nullable=True)
    work_position = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text(), nullable=True)
    is_favorite = db.Column(db.Boolean, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)

    # Stripe customer ID
    customer_id = db.Column(db.String(255), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<ContactsCustomer %s>' % self.id
