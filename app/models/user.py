from app import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, unique=True)

    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    company = db.relationship('Company', backref='users', lazy=True)

    is_active = db.Column(db.Boolean, default=True)
    is_owner = db.Column(db.Boolean, default=False, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    is_member = db.Column(db.Boolean, default=False, nullable=True)
    is_driver = db.Column(db.Boolean, default=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(90), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    DL_number = db.Column(db.String(255), nullable=True)
    DL_state = db.Column(db.String(2), nullable=True)
    DL_expr = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text(), nullable=True)
    password = db.Column(db.String(255), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<User %s>' % self.id
