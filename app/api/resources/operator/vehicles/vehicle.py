from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError

from app import db
from app.models.vehicle import Vehicle
from app.api.schemas.vehicle import VehicleSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate


class VehicleResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        if vehicle_id:
            vehicle = Vehicle.query.filter_by(company_id=company_id,
                                              id=vehicle_id).first()
            res = vehicle_schema.dump(vehicle)
            return jsonify(res), HTTPStatus.OK
        else:
            vehicles = Vehicle.query.filter_by(company_id=company_id)

            return paginate(vehicles, vehicles_schema), HTTPStatus.OK

    def post(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        try:
            vehicle = vehicle_schema.load({**request.get_json(),
                                           'company_id': company_id})
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.add(vehicle)
        db.session.commit()

        return {'msg': 'Vehicle added',
                'vehicle': vehicle_schema.dump(vehicle)}, HTTPStatus.OK

    def put(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        vehicle = Vehicle.query.get_or_404(vehicle_id)

        try:
            vehicle = vehicle_schema.load(request.json, instance=vehicle)
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.commit()

        return {'msg': 'Vehicle information updated',
                'vehicle': vehicle_schema.dump(vehicle)}, HTTPStatus.OK

    def delete(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        vehicle = Vehicle.query.get_or_404(vehicle_id)
        vehicle.is_active = False
        db.session.commit()

        return {'msg': 'Vehicle disabled'}, HTTPStatus.OK


vehicle_schema = VehicleSchema(partial=True)
vehicles_schema = VehicleSchema(many=True)
