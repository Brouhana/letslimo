from app import db
from secrets import choice
from string import ascii_uppercase, ascii_lowercase


class DriverInvite(db.Model):
    __tablename__ = 'driver_invites'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(90), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    DL_number = db.Column(db.String(255), nullable=True)
    DL_state = db.Column(db.String(2), nullable=True)
    DL_expr = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text(), nullable=True)
    has_accepted = db.Column(db.Boolean, default=False)
    invited_by_member_id = db.Column(db.Integer, db.ForeignKey(
        'members.id'), nullable=False)
    invite_code = db.Column(db.String(255), default=''.join(choice(
        ascii_uppercase + ascii_lowercase) for i in range(7)), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<DriverInvite %s>' % self.id
