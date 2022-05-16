from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus

from app.models.company import Company
from app.api.schemas.company import CompanySchema


class CompanyResource(MethodView):
    def get(self, company_id: int):
        company = Company.query.get_or_404(company_id)
        res = company_schema.dump(company)
        return jsonify(res), HTTPStatus.OK

    def put(self, company_id: int):
        company = Company.query.get_or_404(company_id)
        company.update(request.get_json())
        return company_schema.dump(company), HTTPStatus.OK

    def delete(self, company_id: int):
        # A company that is deleted will be marked as inactive
        company = Company.query.get_or_404(company_id)
        company.update({'is_active': False})
        return 'Company disabled', HTTPStatus.OK


company_schema = CompanySchema()
