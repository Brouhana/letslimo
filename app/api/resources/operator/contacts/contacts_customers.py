from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy import func

from app import db
from app.models.contacts_customers import ContactsCustomer
from app.api.schemas.contacts_customer import ContactsCustomerSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate


class ContactsCustomerResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, contacts_customer_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        if contacts_customer_id:
            contacts_customer_id = ContactsCustomer.query.filter_by(
                company_id=company_id, uuid=contacts_customer_id).first()
            res = customer_contact_schema.dump(contacts_customer_id)
            return jsonify(res), HTTPStatus.OK

        param_name = request.args.get('name')

        if param_name:
            query_customer_name_filter = func.lower(ContactsCustomer.full_name).contains(
                func.lower(param_name))
            customer_contacts = ContactsCustomer.query.filter(
                query_customer_name_filter).order_by(ContactsCustomer.full_name)
        else:
            customer_contacts = ContactsCustomer.query.filter_by(
                company_id=company_id).order_by(ContactsCustomer.full_name)

        return paginate(customer_contacts, customer_contacts_schema), HTTPStatus.OK

    def post(self, company_id, contacts_customer_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        try:
            customer_contact = customer_contact_schema.load({**request.get_json(),
                                                             'company_id': company_id})
            customer_contact.full_name = customer_contact.first_name + \
                ' ' + customer_contact.last_name
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.add(customer_contact)
        db.session.commit()

        return {'msg': 'Contact added',
                'company_contact': customer_contact_schema.dump(customer_contact)}, HTTPStatus.OK

    def put(self, company_id, contacts_customer_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        customer_contact = ContactsCustomer.query.get_or_404(
            uuid=contacts_customer_id)

        try:
            customer_contact = customer_contact_schema.load(
                request.json, instance=customer_contact)
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.commit()

        return {'msg': 'Contact updated',
                'company_contact': customer_contact_schema.dump(customer_contact)}, HTTPStatus.OK

    def delete(self, company_id, contacts_customer_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company_contact = ContactsCustomer.query.get_or_404(
            uuid=contacts_customer_id)
        company_contact.is_active = False
        return {'msg': 'Contact disabled'}, HTTPStatus.OK


customer_contact_schema = ContactsCustomerSchema(partial=True)
customer_contacts_schema = ContactsCustomerSchema(many=True)
