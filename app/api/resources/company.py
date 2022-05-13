from flask import (
    request,
    jsonify,
    Blueprint,
    current_app as app
)
from flask.views import MethodView

from app.models.company import Company
from app.api.schemas.company import CompanySchema


class CompanyResource(MethodView):
    def get(self, company_id):
        company = Company.query.filter_by(id=company_id).first()

        if company is None:
            return jsonify({'msg': 'Company not found.'}), 400

        res = CompanySchema().dump(company).data
        return jsonify(res), 200

    def post(self):
        return "Create a new user"

    def put(self, user_id):
        return "Update user"

    def delete(self, user_id):
        return "Delete user"
