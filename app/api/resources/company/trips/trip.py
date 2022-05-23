from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from datetime import datetime
from marshmallow import ValidationError
from sqlalchemy import func

from app import db
from app.models.trips import Trip
from app.api.schemas.trips import TripSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate


class TripResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, trip_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        if trip_id:
            trip = Trip.query.filter_by(
                company_id=company_id, id=trip_id).first()

            return jsonify(trip_schema.dump(trip)), HTTPStatus.OK

        pu_date = request.args.get('pu_date')
        to_date = request.args.get('to_date')
        driver = request.args.get('driver')
        vehicle = request.args.get('vehicle')
        status = request.args.get('status')

        filter_kwargs = {'company_id': company_id}

        if vehicle:
            filter_kwargs['vehicle_id'] = vehicle
        if status:
            filter_kwargs['status'] = status
        if driver:
            filter_kwargs['driver_user_id'] = driver

        if pu_date and to_date:
            # Query trips between pu_date and to_date
            # pu_date is treated as start date, to_date as end
            pu_date = datetime.strptime(pu_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            trips = Trip.query.filter(Trip.pu_datetime.between(
                pu_date, to_date)).filter_by(**filter_kwargs)
        elif pu_date:
            # Query trips on pu_date
            pu_date = datetime.strptime(pu_date, '%Y-%m-%d').date()
            trips = Trip.query.filter(
                func.date(Trip.pu_datetime) == pu_date).filter_by(**filter_kwargs)
        else:
            trips = Trip.query.filter_by(**filter_kwargs)

        return paginate(trips, trips_schema), HTTPStatus.OK

    def post(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        try:
            trip = trip_schema.load(
                {**request.get_json(), 'company_id': company_id})

            db.session.add(trip)
            db.session.commit()

        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        return {'msg': 'Trip scheduled', 'trip': trip_schema.dump(trip)}, HTTPStatus.OK

    def put(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        trip = Trip.query.get_or_404(trip_id)
        trip_stops = request.json.get('stops')

        try:
            trip = trip_schema.load(request.json, instance=trip)

            trip_stops = TripStop.query.filter_by(trip_id=trip_id).all()
            print(trip_stops)
            for stop in trip_stops:
                print(stop)

        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.commit()

        return {'msg': 'Trip information updated',
                'trip': trip_schema.dump(trip)}, HTTPStatus.OK

    def delete(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        trip = Trip.query.get_or_404(trip_id)
        trip.is_active = False
        db.session.commit()

        return {'msg': 'Trip hidden'}, HTTPStatus.OK


trip_schema = TripSchema(partial=True)
trips_schema = TripSchema(many=True)
