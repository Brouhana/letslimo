from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus

from app.models.company import Company
from app.api.schemas.company import CompanySchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company


class CompanyResource(MethodView):
    @role_required('is_member')
    def get(self, company_id: int):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        company = Company.query.get_or_404(company_id)
        res = company_schema.dump(company)
        return jsonify(res), HTTPStatus.OK

    @role_required('is_admin')
    def put(self, company_id: int):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        company = Company.query.get_or_404(company_id)
        company.update(request.get_json())
        return company_schema.dump(company), HTTPStatus.OK

    @role_required('is_admin')
    def delete(self, company_id: int):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        # A company that is deleted will be marked as inactive
        company = Company.query.get_or_404(company_id)
        company.update({'is_active': False})
        return 'Company disabled', HTTPStatus.OK


company_schema = CompanySchema()
