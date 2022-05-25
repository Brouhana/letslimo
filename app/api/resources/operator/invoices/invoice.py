from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError
from datetime import datetime
from sqlalchemy import func, or_

from app import db
from app.models.invoices import Invoice
from app.models.contacts_customers import ContactsCustomer
from app.api.schemas.invoice import InvoiceSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate


class InvoiceResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, invoice_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        if invoice_id:
            invoice = Invoice.query.filter_by(
                company_id=company_id, id=invoice_id).first()

            return jsonify(invoice_schema.dump(invoice)), HTTPStatus.OK

        param_is_overdue = request.args.get('is_overdue')
        param_contact = request.args.get('contact')
        param_invoiced_on = request.args.get('invoiced_on')
        param_status = request.args.get('status')

        filter_kwargs = {'company_id': company_id}

        if param_status:
            filter_kwargs['status'] = param_status

        if param_contact:
            ContactsCustomer.query.join(Invoice).filter(or_(Invoice.first_name.contains(
                param_contact), Invoice.last_name.contains(param_contact))).all()

        if param_invoiced_on:
            invoiced_on_date = datetime.strptime(
                param_invoiced_on, '%Y-%m-%d').date()
            invoices = Invoice.query.filter(
                func.date(Invoice.created_at) == invoiced_on_date).filter_by(**filter_kwargs)

        if param_is_overdue:
            today_date_utc = datetime.utcnow().date()
            invoices = Invoice.query.filter(
                Invoice.due_on > today_date_utc).filter_by(**filter_kwargs)
        else:
            invoices = Invoice.query.filter_by(**filter_kwargs)

        return paginate(invoices, invoices_schema), HTTPStatus.OK

    def post(self, company_id, invoice_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        try:
            invoice = invoice_schema.load(
                {**request.get_json(), 'company_id': company_id})

            db.session.add(invoice)
            db.session.commit()

        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        return {'msg': 'Invoice created', 'invoice': invoice_schema.dump(invoice)}, HTTPStatus.OK

    def put(self, company_id, invoice_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        return '', HTTPStatus.OK

    def delete(self, company_id, invoice_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        return '', HTTPStatus.OK


invoice_schema = InvoiceSchema(partial=True)
invoices_schema = InvoiceSchema(many=True)
