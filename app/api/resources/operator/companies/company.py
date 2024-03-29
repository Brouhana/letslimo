from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError

from app import db
from app.models.company import Company
from app.api.schemas.company import CompanySchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company


class CompanyResource(MethodView):
    @role_required('member')
    def get(self, company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company = Company.query.get_or_404(company_id)
        res = company_schema.dump(company)
        return jsonify(res), HTTPStatus.OK

    @role_required('admin')
    def put(self, company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company = Company.query.get_or_404(company_id)

        try:
            company = company_schema.load(request.json, instance=company)
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.commit()

        return {'msg': 'Company information updated',
                'company': company_schema.dump(company)}, HTTPStatus.OK

    @role_required('owner')
    def delete(self, company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company = Company.query.get_or_404(company_id)
        company.is_active = False
        return {'msg': 'Company disabled'}, HTTPStatus.OK


company_schema = CompanySchema(partial=True)
