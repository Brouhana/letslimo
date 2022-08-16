from app import ma, db
from app.models.driver_payouts import DriverPayout
from app.api.schemas.trips import TripSchema
from app.api.schemas.user import UserSchema
from marshmallow import fields


class DriverPayoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DriverPayout
        sqla_session = db.session
        load_instance = True
        include_fk = True

    company_id = fields.Integer(required=True)
    driver = fields.Nested(
        UserSchema,
        exclude=('created_on',
                 'last_updated',
                 'company_id',
                 'password',
                 'id',
                 'is_admin',
                 'is_owner',
                 'is_driver',
                 'email',
                 'address',),
        required=False)
    trip = fields.Nested(
        TripSchema,
        exclude=('created_on',
                 'last_updated',
                 'company_id',),
        required=True)
    flat_rate = fields.Float(required=False)
    hourly_rate = fields.Float(required=False)
    hours = fields.Float(required=False)
    gratuity = fields.Float(required=False)
    total = fields.Float(required=False)
