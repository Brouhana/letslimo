from flask import (
    request,
    jsonify,
    current_app as app
)
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus

from app import db
from app.models.user import User
from app.models.company import Company
from app.models.user_invites import UserInvite
from app.api.schemas.user import UserSchema
from app.commons.pagination import paginate
from app.commons.helpers import can_access_company
from app.commons.mail import send_mail
from app.middleware.role_required import role_required


class UserResource(MethodView):
    @role_required('member')
    def get(self, company_id, user_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

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
                return jsonify({'msg': 'Invalid user type.'}), HTTPStatus.BAD_REQUEST

            return paginate(users, users_schema), HTTPStatus.OK

    @role_required('member')
    def post(self, company_id, user_id):
        if not can_access_company(company_id):
            return jsonify({'msg': 'You are not authorized to access this company.'}), HTTPStatus.UNAUTHORIZED

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
        company_id = get_jwt_identity()['company_id']
        invited_by_user_id = get_jwt_identity()['user_id']

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
                                  company_id=company_id,
                                  invited_by_user_id=invited_by_user_id))
        db.session.commit()

        company = Company.query.filter_by(id=company_id).first()
        invite = UserInvite.query.filter_by(email=email).first()
        send_mail(email,
                  'You are invited to join {} on Let\'sLimo'.format(
                      company.company_name),
                  'Hi {},<br/><br/>You have been added to drive for {} on Let\'sLimo.<br/><br/>To get started, create your account. \
                      Your setup code is {}.<br/><br/>Have a great day!'.format(first_name, company.company_name, invite.invite_code))

        return 'New user invite created', HTTPStatus.CREATED

    def put(self, company_id, user_id):
        return "Update user"

    def delete(self, company_id, user_id):
        return "Delete user"


user_schema = UserSchema()
users_schema = UserSchema(many=True)
