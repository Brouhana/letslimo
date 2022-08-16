from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus
import stripe
from os import environ

from app import db
from app.models.company import Company
from app.middleware.role_required import role_required
from app.commons.helpers import can_access_company


class PaymentSetupResource(MethodView):
    decorators = [role_required('member')]

    stripe.api_key = environ.get('STRIPE_TEST_API_KEY')

    def get(self, company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company = Company.query.filter_by(id=company_id).first()

        stripe_account_id = company.connected_account
        return stripe.Account.retrieve(stripe_account_id)

    def post(self, company_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        company = Company.query.filter_by(id=company_id).first()

        req = request.get_json()

        business_type = req['business_type']
        if company.company_website_url is not None:
            business_profile = {
                "url": company.company_website_url, "mcc": "4121"}
        else:
            business_profile = {
                "product_description": company.company_name + ' is a ground transportation operator.', "mcc": "4121"}

        if company.connected_account:
            stripe_account_id = company.connected_account
        else:
            create_stripe_account = stripe.Account.create(
                country="US",
                type="express",
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
                business_type=business_type,
                business_profile=business_profile,
            )
            stripe_account_id = create_stripe_account['id']
            try:
                company.connected_account = stripe_account_id
                db.session.commit()
            except Exception:
                return jsonify({'msg': 'Error adding connected account ID to Company'}), HTTPStatus.INTERNAL_SERVER_ERROR

        create_stripe_account_link = stripe.AccountLink.create(
            account=company.connected_account,
            refresh_url="http://localhost:3000/settings/payments",
            return_url="http://localhost:3000/settings/payments",
            type="account_onboarding",
        )
        return create_stripe_account_link, HTTPStatus.OK
