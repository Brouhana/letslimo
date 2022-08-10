from time import strftime
from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from datetime import datetime, timedelta
from marshmallow import ValidationError
from sqlalchemy import func
import psycopg2.extras
from secrets import token_urlsafe

from app import db
from app.models.trips import Trip
from app.models.trip_groups import TripGroup
from app.api.schemas.trips import TripSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate
from app.commons.mail import send_reservation_conf
# from app.commons.localdatetime import tz_diff_hours


class TripResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, trip_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        if trip_id:
            trip = Trip.query.filter_by(
                company_id=company_id, uuid=trip_id).first()
            tripgroup = {'group': trips_schema.dump(trip.tripgroup.trips)}
            return jsonify(trip_schema.dump(trip), tripgroup), HTTPStatus.OK

        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        driver = request.args.get('driver')
        vehicle = request.args.get('vehicle')
        status = request.args.get('status')
        trip_code_sub = request.args.get('trip_code')

        filter_kwargs = {'company_id': company_id}

        if vehicle:
            filter_kwargs['vehicle_id'] = vehicle
        if status:
            filter_kwargs['status'] = status
        if driver:
            filter_kwargs['driver_user_id'] = driver
            if driver == 'unassigned':
                filter_kwargs['driver_user_id'] = None

        # convert to datetimes
        # adjust for UTC to Local TZ hours difference
        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            from_date_UTCstart = (from_date + timedelta(hours=5))
            from_date_UTCend = (
                from_date + timedelta(days=1, hours=5))
        if to_date:
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
            to_date_UTCend = (to_date + timedelta(days=1, hours=4))

        if from_date and to_date:
            trips = Trip.query.filter(Trip.pu_datetime.between(
                from_date_UTCstart, to_date_UTCend)).order_by(Trip.pu_datetime)
        elif from_date:
            trips = Trip.query.filter(
                Trip.pu_datetime.between(from_date_UTCstart, from_date_UTCend)).order_by(Trip.pu_datetime)
        else:
            trips = Trip.query.order_by(
                Trip.pu_datetime)

        if trip_code_sub:
            trip_code_sub = trip_code_sub.upper()
            trips = Trip.query.filter(
                Trip.trip_code_sub.contains(trip_code_sub))

        trips = trips.filter_by(**filter_kwargs)

        return paginate(trips, trips_schema), HTTPStatus.OK

    def post(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        can_send_email = request.args.get('email')

        try:
            # prevents psycopg2.ProgrammingError can't adapt type 'dict' errror
            psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
            trip = trip_schema.load(
                {**request.get_json(), 'company_id': company_id})
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            if trip.tripgroup_id is not None:
                trip_group = TripGroup.query.filter_by(
                    id=trip.tripgroup_id).first()
            else:
                trip_code = ''.join([c for c in token_urlsafe(10)
                                    if c not in '-_abcdefghijklmnopqrstuvwxyzO0lI'])[:4]
                trip_group = TripGroup(company_id=company_id,
                                       trip_code=trip_code)
                db.session.add(trip_group)
                db.session.flush()
                trip.tripgroup_id = trip_group.id

            trip_sub_code = ''.join([c for c in token_urlsafe(
                10) if c not in '-_abcdefghijklmnopqrstuvwxyzO0lI'])[:3]
            trip.trip_code_sub = trip_group.trip_code + '-' + trip_sub_code

            db.session.add(trip)
            db.session.commit()

            # returntrip is implicity implied by the presence of parenttrip_id
            # If parenttrip_id is supplied, then assign query the parent trip
            # and update parent's roundtrip_id to the id of the new trip
            if trip.parenttrip_id:
                parent_trip = Trip.query.filter_by(
                    company_id=company_id, id=trip.parenttrip_id).first()
                parent_trip.returntrip_id = trip.id
                db.session.commit()
        except Exception:
            return {'msg': 'Error adding trip'}, HTTPStatus.INTERNAL_SERVER_ERROR

        if (can_send_email):
            send_reservation_conf(trip=trip)

        return {'msg': 'Trip scheduled', 'trip': trip_schema.dump(trip)}, HTTPStatus.OK

    def put(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        trip = Trip.query.filter_by(company_id=company_id,
                                    uuid=trip_id).first()
        try:
            trip = trip_schema.load(request.json, instance=trip)
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.commit()
        return {'msg': 'Trip information updated',
                'trip': trip_schema.dump(trip)}, HTTPStatus.OK

    def delete(self, company_id, trip_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        trip = Trip.query.filter_by(company_id=company_id,
                                    uuid=trip_id).first()
        trip.is_active = False
        db.session.commit()
        return {'msg': 'Trip hidden'}, HTTPStatus.OK


trip_schema = TripSchema(partial=True)
trips_schema = TripSchema(many=True)
