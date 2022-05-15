from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from http import HTTPStatus

from app import db
from app.models.company import Company
from app.models.user import User
from app.models.user_invites import UserInvite
from app.api.schemas.user import UserSchema
from app.commons.pagination import paginate


class UserResource(MethodView):
    def get(self, company_id: int, user_id: int):
        user_type = request.args.get('user_type')

        company = Company.query.get_or_404(company_id)

        if user_type == 'driver':
            users = User.query.filter_by(company_id=company_id, is_driver=True)

        if user_type == 'member':
            users = User.query.filter_by(company_id=company_id, is_member=True)

        return paginate(users, users_schema)

    def post(self, company_id: int):
        if not request.is_json:
            return jsonify({'msg': 'Invalid request format.'}), HTTPStatus.BadRequest

        company = Company.query.get_or_404(company_id)

        # TODO: Validate that company.id matches requester's company id

        is_owner = request.json.get('is_owner', False)
        is_admin = request.json.get('is_admin', False)
        is_member = request.json.get('is_member', False)
        is_driver = request.json.get('is_driver', True)
        email = request.json.get('email', None)
        first_name = request.json.get('first_name', None)
        last_name = request.json.get('last_name', None)
        phone = request.json.get('phone', None)
        address = request.json.get('address', None)
        DL_number = request.json.get('DL_number', None)
        DL_state = request.json.get('DL_state', None)
        DL_expr = request.json.get('DL_expr', None)
        notes = request.json.get('notes', None)
        # TODO: get requester's id
        invited_by_user_id = request.json.get('invited_by_user_id', None)

        if email is None or first_name is None or last_name is None or phone is None:
            return jsonify({'msg': 'Missing required fields.'}), HTTPStatus.BadRequest

        db.session.add(UserInvite(is_owner=is_owner,
                                  is_admin=is_admin,
                                  is_member=is_member,
                                  is_driver=is_driver,
                                  email=email,
                                  first_name=first_name,
                                  last_name=last_name,
                                  phone=phone,
                                  address=address,
                                  DL_number=DL_number,
                                  DL_state=DL_state,
                                  DL_expr=DL_expr,
                                  notes=notes,
                                  invited_by_user_id=invited_by_user_id))
        db.session.commit()

        # TODO: send email to invitee's email with invite_code

        return 'New user invite created', HTTPStatus.CREATED

    def put(self, company_id: int, user_id: int):
        return "Update user"

    def delete(self, company_id: int, user_id: int):
        return "Delete user"


user_schema = UserSchema()
users_schema = UserSchema(many=True)
