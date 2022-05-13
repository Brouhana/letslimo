from app import db
import secrets
import string


class OperatorUser(db.Model):
    __tablename__ = 'operator_users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(90), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_owner = db.Column(db.Boolean, default=False, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    is_member = db.Column(db.Boolean, default=True, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    creation_code = db.Column(db.String(255), default=''.join(secrets.choice(
        string.ascii_uppercase + string.ascii_lowercase) for i in range(7)), nullable=True)
    password = db.Column(db.String(255), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<OperatorUser %s>' % self.email
