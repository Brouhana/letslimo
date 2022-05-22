from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from datetime import date, datetime
from marshmallow import ValidationError
from sqlalchemy import func

from app import db
from app.models.trips import Trip
from app.models.trips_stops import TripStop
from app.api.schemas.trips.trips import TripSchema
from app.api.schemas.trips.trips_stops import TripStopSchema
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

            if trip.has_stops:
                stops = TripStop.query.filter_by(company_id=company_id,
                                                 trip_id=trip_id)
                res = {**trip_schema.dump(trip),
                       'stops': trip_stops_schema.dump(stops)}

            if not trip.has_stops:
                res = trip_schema.dump(trip)

            return jsonify(res), HTTPStatus.OK

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

            trip_stops = request.json.get('stops')

            db.session.add(trip)
            trip.has_stops = True if trip_stops else False
            db.session.commit()

            if trip_stops:
                # Query trip just added for trip_id
                # Then for all stops, serialize and add to trip_stops table
                trip = Trip.query.filter_by(
                    company_id=company_id).order_by(Trip.id.desc()).first()

                for stop in trip_stops:
                    trip_stop = trip_stop_schema.load(
                        {**stop, 'trip_id': trip.id, 'company_id': company_id})

                    db.session.add(trip_stop)
                    db.session.commit()

        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        return {'msg': 'Trip scheduled', 'trip': trip_schema.dump(trip)}, HTTPStatus.OK

    def put(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        return ''

    def delete(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        return ''


trip_schema = TripSchema()
trips_schema = TripSchema(many=True)
trip_stop_schema = TripStopSchema()
trip_stops_schema = TripStopSchema(many=True)
