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
import psycopg2.extras

from app import db
from app.models.trips import Trip
from app.models.company import Company
from app.models.vehicle import Vehicle
from app.models.contacts_customers import ContactsCustomer
from app.api.schemas.trips import TripSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate
from app.commons.mail import send_reservation_conf
import json


class TripResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, trip_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        if trip_id:
            trip = Trip.query.filter_by(company_id=company_id,
                                        uuid=trip_id).first()

            return jsonify(trip_schema.dump(trip)), HTTPStatus.OK

        from_date = request.args.get('from_date')
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

        if from_date and to_date:
            # Query trips between from_date and to_date
            # from_date is treated as start date, to_date as end
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            trips = Trip.query.filter(Trip.pu_datetime.between(
                from_date, to_date)).order_by(Trip.pu_datetime).filter_by(**filter_kwargs)
        elif from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            trips = Trip.query.filter(
                func.date(Trip.pu_datetime) == from_date).order_by(Trip.pu_datetime).filter_by(**filter_kwargs)
        else:
            trips = Trip.query.order_by(
                Trip.pu_datetime).filter_by(**filter_kwargs)

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
            trip.pu_datetime = datetime.strptime(trip.pu_datetime,
                                                 "%a %b %d %Y %H:%M:%S")

            if (can_send_email):
                company = Company.query.filter_by(
                    id=company_id).first()
                contacts_customer = ContactsCustomer.query.filter_by(
                    id=trip.contacts_customer_id).first()
                vehicle = Vehicle.query.filter_by(
                    id=trip.vehicle_id).first()

                if (contacts_customer is None):
                    return {'msg': 'Error getting customer contact'}, HTTPStatus.INTERNAL_SERVER_ERROR

                send_reservation_conf(to=contacts_customer.email,
                                      company_name=company.company_name,
                                      booking_contact_name=contacts_customer.first_name,
                                      vehicle=vehicle.name,
                                      pu_date=trip.pu_datetime.strftime(
                                          "%m/%d/%Y"),
                                      pu_time=trip.pu_datetime.strftime(
                                          "%H:%M:%S"),
                                      passenger_name=contacts_customer.first_name,
                                      company_email=company.company_booking_email,
                                      company_phone=company.company_phone,
                                      company_address=company.company_address)

        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.add(trip)
        db.session.commit()

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
