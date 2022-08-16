from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
from marshmallow import ValidationError
from sqlalchemy import func

from app import db
from app.models.company import Company
from app.models.driver_payouts import DriverPayout
from app.api.schemas.driver_payout import DriverPayoutSchema
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company
from app.commons.pagination import paginate


class DriverPayoutResource(MethodView):
    decorators = [role_required('member')]

    def get(self, company_id, payout_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        if payout_id:
            payout = DriverPayout.query.filter_by(
                company_id=company_id, id=payout_id).first()

            return jsonify(driver_payout_schema.dump(payout)), HTTPStatus.OK

        filter_kwargs = {'company_id': company_id}
        driver_payouts = DriverPayout.query.filter_by(**filter_kwargs)
        return paginate(driver_payouts, driver_payouts_schema), HTTPStatus.OK

    def post(self, company_id, payout_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        try:
            payout = driver_payout_schema.load(
                {**request.get_json(), 'company_id': company_id})
            db.session.add(payout)
            db.session.commit()
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        return {'msg': 'Payout created', 'driver_payout': driver_payout_schema.dump(payout)}, HTTPStatus.OK

    def put(self, company_id, payout_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        payout = DriverPayout.query.filter_by(
            company_id=company_id, id=payout_id)
        try:
            payout = driver_payout_schema.load(request.json, instance=payout)
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.commit()

        return {'msg': 'Payout updated',
                'driver_payout': driver_payout_schema.dump(payout)}, HTTPStatus.OK

    # def delete(self, company_id, payout_id):
    #     if not can_access_company(company_id):
    #         return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

    #     payout = DriverPayout.query.filter_by(
    #         company_id=company_id, id=payout_id)
    #     db.session.delete(payout)
    #     db.session.commit()

    #     return 'Payout deleted', HTTPStatus.OK


driver_payout_schema = DriverPayoutSchema(partial=True)
driver_payouts_schema = DriverPayoutSchema(many=True)
