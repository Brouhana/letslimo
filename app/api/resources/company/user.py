from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus
from marshmallow import ValidationError

from app import db
from app.models.user import User
from app.models.user_invites import UserInvite
from app.api.schemas.user import UserSchema
from app.api.schemas.user_invite import UserInviteSchema
from app.commons.pagination import paginate
from app.commons.helpers import can_access_company
from app.commons.mail import send_invite
from app.middleware.role_required import role_required


class UserResource(MethodView):
    @role_required('member')
    def get(self, company_id, user_id):
        if not can_access_company(company_id):
            return {'msg': 'You are not authorized to access this company.'}, HTTPStatus.UNAUTHORIZED

        if user_id:
            user = User.query.filter_by(
                company_id=company_id, id=user_id).first()
            res = user_schema.dump(user)
            return jsonify(res), HTTPStatus.OK
        else:
            user_type = request.args.get('user_type')

            if user_type == 'driver':
                users = User.query.filter_by(company_id=company_id,
                                             is_driver=True)
            elif user_type == 'member':
                users = User.query.filter_by(company_id=company_id,
                                             is_member=True)
            else:
                return {'msg': 'Invalid user type.'}, HTTPStatus.BAD_REQUEST

            return paginate(users, users_schema), HTTPStatus.OK

    @role_required('member')
    def post(self, company_id, user_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

        user_invite_schema = UserInviteSchema()
        invited_by_user_id = get_jwt_identity()['user_id']
        company_id = get_jwt_identity()['company_id']

        try:
            invitee = user_invite_schema.load({**request.get_json(),
                                               'company_id': company_id,
                                               'invited_by_user_id': invited_by_user_id})
            # Validate email is unique
            if UserInvite.query.filter_by(email=invitee.email).first() is not None:
                return {'error': 'Email already exists.'}, HTTPStatus.UNPROCESSABLE_ENTITY
        except ValidationError as err:
            return {'errors': err.messages}, HTTPStatus.UNPROCESSABLE_ENTITY

        db.session.add(invitee)
        db.session.commit()

        # Send email to invitee with invite code
        send_invite(to=invitee.email,
                    invitee_first_name=invitee.first_name,
                    invitee_last_name=invitee.last_name,
                    inviter_full_name=get_jwt_identity(
                    )['first_name'] + ' ' + get_jwt_identity()['last_name'],
                    company_name=invitee.company.company_name,
                    invite_code=invitee.invite_code,
                    type='member' if invitee.is_member else 'driver')

        return {'msg': '{} has been invited.'.format(invitee.email),
                'invitee': user_invite_schema.dump(invitee)}, HTTPStatus.OK

    def put(self, company_id, user_id):
        return "Update user"

    def delete(self, company_id, user_id):
        return "Delete user"


user_schema = UserSchema(partial=True)
users_schema = UserSchema(many=True)
