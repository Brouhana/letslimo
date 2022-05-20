from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError

from app import db
from app.models.contacts_companies import ContactsCompany
from app.api.schemas.contacts.contacts_company import ContactsCompanySchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate


class ContactsCompanyResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, company_contact_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        if company_contact_id:
            company_contact = ContactsCompany.query.filter_by(
                company_id=company_id, id=company_contact_id).first()
            res = company_contact_schema.dump(company_contact)
            return jsonify(res), HTTPStatus.OK
        else:
            company_contacts = ContactsCompany.query.filter_by(
                company_id=company_id)

            return paginate(company_contacts, company_contacts_schema), HTTPStatus.OK

    def post(self, company_id, company_contact_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        try:
            company_contact = company_contact_schema.load({**request.get_json(),
                                                           'company_id': company_id})
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.add(company_contact)
        db.session.commit()

        return {'msg': 'Contact added',
                'company_contact': company_contact_schema.dump(company_contact)}, HTTPStatus.OK

    def put(self, company_id, company_contact_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company_contact = ContactsCompany.query.get_or_404(company_contact_id)

        try:
            company_contact = company_contact_schema.load(
                request.json, instance=company_contact)
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.commit()

        return {'msg': 'Contact updated',
                'company_contact': company_contact_schema.dump(company_contact)}, HTTPStatus.OK

    def delete(self, company_id, company_contact_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company_contact = ContactsCompany.query.get_or_404(company_contact_id)
        company_contact.is_active = False
        return {'msg': 'Contact disabled'}, HTTPStatus.OK


company_contact_schema = ContactsCompanySchema(partial=True)
company_contacts_schema = ContactsCompanySchema(many=True)
