from app import db


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(90), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    is_owner = db.Column(db.Boolean, default=False, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<Member %s>' % self.email
