from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView

from app.models.company import Company
from app.api.schemas.company import CompanySchema


class CompanyResource(MethodView):
    def get(self, company_id: int):
        company = Company.query.get_or_404(company_id)
        res = company_schema.dump(company)
        return jsonify(res), 200

    def put(self, company_id: int):
        company = Company.query.get_or_404(company_id)

        if not request.is_json:
            return jsonify({'msg': 'Invalid request format.'}), 400

        company.update(request.get_json())
        return company_schema.dump(company), 200

    def delete(self, company_id: int):
        return "Delete company by id"


company_schema = CompanySchema()
