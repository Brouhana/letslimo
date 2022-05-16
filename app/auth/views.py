from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_bcrypt import check_password_hash
from http import HTTPStatus

from app import db, bcrypt
from app.models.user import User
from app.models.user_invites import UserInvite


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.post('/login')
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if email is None or password is None:
        return jsonify({'msg': 'Email or password is empty.'}), HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({'msg': 'Incorrect email or password.'}), HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(
        identity={'id': user.id, 'company': user.company_id})
    refresh_token = create_refresh_token(
        identity={'id': user.id, 'company': user.company_id})

    res = {'access_token': access_token, 'refresh_token': refresh_token}
    return jsonify(res), HTTPStatus.OK


@auth_bp.post('/register_invitee')
def register_invitee():
    email = request.json.get('email', None)
    invite_code = request.json.get('invite_code', None)
    password = request.json.get('password', None)

    if email is None or invite_code is None or password is None:
        return jsonify({'msg': 'Missing required fields.'}), HTTPStatus.BAD_REQUEST

    invitee = UserInvite.query.filter_by(email=email).first()

    if invitee is None:
        return jsonify({'msg': 'There is no invite for you yet.'}), HTTPStatus.NOT_FOUND

    # Invitee must have not already accepted the invite
    if invitee.has_accepted:
        return jsonify({'msg': 'You have already accepted the invite.'}), HTTPStatus.BAD_REQUEST

    # Request's invite code must match the invitee's invite code
    if invitee.invite_code != invite_code:
        return jsonify({'msg': 'Invalid invite code.'}), HTTPStatus.UNAUTHORIZED

    password = bcrypt.generate_password_hash(password, 14).decode('utf-8')

    # Create new user with data from UserInvite record
    db.session.add(User(company_id=invitee.company_id,
                        is_owner=invitee.is_owner,
                        is_admin=invitee.is_admin,
                        is_member=invitee.is_member,
                        is_driver=invitee.is_driver,
                        email=invitee.email,
                        first_name=invitee.first_name,
                        last_name=invitee.last_name,
                        phone=invitee.phone,
                        address=invitee.address,
                        DL_number=invitee.DL_number,
                        DL_state=invitee.DL_state,
                        DL_expr=invitee.DL_expr,
                        notes=invitee.notes,
                        password=password))

    # As a User has been created, consider the invitee has accepted the invite
    invitee.has_accepted = True

    db.session.commit()

    return jsonify({'msg': 'Successfully registered.'}), HTTPStatus.OK
