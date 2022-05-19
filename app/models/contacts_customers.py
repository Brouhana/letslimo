from app import db


class ContactsCustomer(db.Model):
    __tablename__ = 'contacts_customers'

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    company = db.relationship('Company', backref='customers', lazy=True)

    first_name = db.Column(db.String(90), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), nullable=False)

    contacts_company_id = db.Column(db.Integer, db.ForeignKey(
        'contacts_companies.id'), nullable=True)
    contacts_company = db.relationship(
        'Company', backref='contacts_customers', lazy=True)

    home_address = db.Column(db.String(255), nullable=True)
    work_address = db.Column(db.String(255), nullable=True)
    work_position = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text(), nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
