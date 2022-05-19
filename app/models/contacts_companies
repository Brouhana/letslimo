from app import db


class ContactsCompany(db.Model):
    __tablename__ = 'contacts_companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    website_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    is_favorite = db.Column(db.Boolean(), default=False, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<ContactsCompany %s>' % self.id
