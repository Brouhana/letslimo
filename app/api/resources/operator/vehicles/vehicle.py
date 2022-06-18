from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError
import uuid
from sqlalchemy import func
from sqlalchemy.types import Unicode

from app import db
from app.models.vehicle import Vehicle
from app.api.schemas.vehicle import VehicleSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate
from app.commons.object_storage import upload_file


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
            param_name = request.args.get('name')
            param_pax = request.args.get('pax')
            param_vehicle_type = request.args.get('vehicle_type')

            vehicles = Vehicle.query.filter_by(company_id=company_id)

            if param_name:
                query_vehicle_name_filter = func.lower(Vehicle.name).contains(
                    func.lower(param_name))
                vehicles = vehicles.filter(query_vehicle_name_filter)

            if param_pax:
                query_vehicle_pax_filter = Vehicle.pax_capacity >= param_pax
                vehicles = vehicles.filter(query_vehicle_pax_filter)

            if param_vehicle_type:
                query_vehicle_type_filter = Vehicle.vehicle_type[0]['type'].astext.cast(
                    Unicode) == param_vehicle_type
                vehicles = vehicles.filter(query_vehicle_type_filter)

            return paginate(vehicles, vehicles_schema), HTTPStatus.OK

    def post(self, company_id, vehicle_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        try:
            vehicle = vehicle_schema.load({**request.get_json(),
                                           'company_id': company_id})

            # For every photo present, upload it to S3-compatible storage
            # key assigns a random UUID filename to the object
            if vehicle.photo1:
                vehicle.photo1 = upload_file(
                    key=uuid.uuid4().hex + '.jpeg', body=vehicle.photo1, is_base64=True)
            if vehicle.photo2:
                vehicle.photo2 = upload_file(
                    key=uuid.uuid4().hex + '.jpeg', body=vehicle.photo2, is_base64=True)
            if vehicle.photo3:
                vehicle.photo3 = upload_file(
                    key=uuid.uuid4().hex + '.jpeg', body=vehicle.photo3, is_base64=True)

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
