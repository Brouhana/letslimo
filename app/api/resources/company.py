from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView

from app import db
from app.models.company import Company
from app.api.schemas.company import CompanySchema


class CompanyResource(MethodView):
    def get(self, company_id: int):
        company = Company.query.get_or_404(company_id)
        res = company_schema.dump(company)
        return jsonify(res), 200

    def put(self, company_id: int):
        company = Company.query.get_or_404(company_id)
        # company = company_schema.load(request.json, instance=company)

        # db.session.commit()

        return company_schema.dump(company), 200

    def delete(self, company_id: int):
        return "Delete user"


company_schema = CompanySchema()
