from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus

from app.models.vehicle import Vehicle
from app.api.schemas.vehicle import VehicleSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company


class VehicleResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        return jsonify('get'), HTTPStatus.OK

    def post(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        return jsonify('post'), HTTPStatus.OK

    def put(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        return jsonify('put'), HTTPStatus.OK

    def delete(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        return jsonify('delete'), HTTPStatus.OK


vehicle_schema = VehicleSchema()
