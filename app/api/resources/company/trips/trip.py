from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError

from app import db
from app.models.trips import Trip
from app.api.schemas.trips.trips import TripSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate


class TripResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, trip_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        return ''

    def post(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        # try:
        #     trip = trip_schema.load({**request.get_json(),
        #                              'company_id': company_id})

        #     if trip.has_stops:
        #         print('has_stops', trip.has_stops)
        # except ValidationError as err:
        #     return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        # db.session.add(trip)
        # db.session.commit()

        # return {'msg': 'Trip scheduled',
        #         'trip': trip_schema.dump(trip)}, HTTPStatus.OK

    def put(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        return ''

    def delete(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        return ''


trip_schema = TripSchema(partial=True)
trips_schema = TripSchema(many=True)
