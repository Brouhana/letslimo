from app import ma, db
from app.models.company import Company
from marshmallow import fields, validate


class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        sqla_session = db.session
        load_instance = True

    is_active = fields.Boolean(is_required=False)
    company_name = fields.String(
        is_required=False, validate=validate.Length(max=255))
    company_address = fields.String(
        is_required=False, validate=validate.Length(max=255))
    company_website_url = fields.URL(is_required=False)
    company_general_email = fields.Email(is_required=False)
    company_booking_email = fields.Email(is_required=False)
    setting_timezone = fields.URL(is_required=True)
    phone = fields.String(required=True, validate=validate.Length(max=20))
