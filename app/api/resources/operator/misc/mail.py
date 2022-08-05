from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError
from datetime import datetime
from sqlalchemy import func, or_, and_

from app import db
from app.models.invoices import Invoice
from app.models.contacts_customers import ContactsCustomer
from app.models.trips import Trip
from app.models.company import Company
from app.api.schemas.invoice import InvoiceSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate
from app.commons.mail import send_reservation_conf


class MailResource(MethodView):
    decorators = [role_required('member')]

    def post(self, company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        req = request.get_json()
        is_trip = request.args.get('trip')

        try:
            # trip_id present: send reservation confirmation email
            if is_trip == '1':
                trip_id = req['trip_id']
                trip = Trip.query.filter_by(company_id=company_id,
                                            uuid=trip_id).first()
                send_reservation_conf(trip)
                return {'msg': 'Email sent'}, HTTPStatus.OK
        except Exception:
            return {'msg': 'Error sending email'}, HTTPStatus.OK
