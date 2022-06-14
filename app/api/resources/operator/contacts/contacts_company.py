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
from app.models.contacts_companies import ContactsCompany
from app.api.schemas.contacts_company import ContactsCompanySchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate


class ContactsCompanyResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, contacts_company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        if contacts_company_id:
            company_contact = ContactsCompany.query.filter_by(
                company_id=company_id, uuid=contacts_company_id).first()
            res = company_contact_schema.dump(company_contact)
            return jsonify(res), HTTPStatus.OK

        param_name = request.args.get('name')

        if param_name:
            query_customer_name_filter = func.lower(ContactsCompany.name).contains(
                func.lower(param_name))
            company_contacts = ContactsCompany.query.filter(
                query_customer_name_filter).order_by(ContactsCompany.name)
        else:
            company_contacts = ContactsCompany.query.filter_by(
                company_id=company_id).order_by(ContactsCompany.name)

        return paginate(company_contacts, company_contacts_schema), HTTPStatus.OK

    def post(self, company_id, contacts_company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        try:
            company_contact = company_contact_schema.load({**request.get_json(),
                                                           'company_id': company_id})
            company_contact.name = company_contact.name.strip()
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.add(company_contact)
        db.session.commit()

        return {'msg': 'Contact added',
                'company_contact': company_contact_schema.dump(company_contact)}, HTTPStatus.OK

    def put(self, company_id, contacts_company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company_contact = ContactsCompany.query.filter_by(
            company_id=company_id, uuid=contacts_company_id).first()

        try:
            company_contact = company_contact_schema.load(
                request.json, instance=company_contact)
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.commit()

        return {'msg': 'Contact updated',
                'company_contact': company_contact_schema.dump(company_contact)}, HTTPStatus.OK

    def delete(self, company_id, contacts_company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company_contact = ContactsCompany.query.filter_by(
            company_id=company_id, uuid=contacts_company_id)
        company_contact.is_active = False
        return {'msg': 'Contact disabled'}, HTTPStatus.OK


company_contact_schema = ContactsCompanySchema(partial=True)
company_contacts_schema = ContactsCompanySchema(many=True)
