from app import db
from secrets import choice
from string import ascii_uppercase, ascii_lowercase


class MemberInvite(db.Model):
    __tablename__ = 'member_invites'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'companies.id'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(90), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    is_owner = db.Column(db.Boolean, default=False, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    has_accepted = db.Column(db.Boolean, default=False)
    invited_by_member_id = db.Column(db.Integer, db.ForeignKey(
        'members.id'), nullable=False)
    invite_code = db.Column(db.String(255), default=''.join(choice(
        ascii_uppercase + ascii_lowercase) for i in range(7)), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    last_updated = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return '<MemberInvite %s>' % self.email
