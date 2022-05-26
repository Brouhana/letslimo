from app import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    company = db.relationship(
        'Company', backref='invoices', lazy=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    trip = db.relationship('Trip', backref='invoices', lazy=True)
    contacts_customer_id = db.Column(db.Integer, db.ForeignKey(
        'contacts_customers.id'), nullable=False)
    contacts_customer = db.relationship(
        'ContactsCustomer', backref='invoices', lazy=True)
    amount_due = db.Column(db.Float, nullable=False)
    message = db.Column(db.Text(), nullable=True)
    due_on = db.Column(db.DateTime, nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())
