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


# @auth_bp.post('/login')
# def login():
#     """
#     Authenticates a user's credentials and returns tokens
#     """
#     if not request.is_json:
#         return jsonify({'msg': 'Invalid request format.'}), 400

#     email = request.json.get('email', None)
#     password = request.json.get('password', None)

#     if not email or not password:
#         return jsonify({'msg': 'Email or password is empty.'}), 400

#     user = User.query.filter_by(email=email).first()

#     if user is None or not check_password_hash(user.password, password):
#         return jsonify({'msg': 'Incorrect email or password.'}), 401

#     access_token = create_access_token(
#         identity={'id': user.id, 'company': user.company_id})
#     refresh_token = create_refresh_token(
#         identity={'id': user.id, 'company': user.company_id})

#     res = {"access_token": access_token, "refresh_token": refresh_token}

#     return jsonify(res), 200


# @auth_bp.post('/register')
# def register():
#     if not request.is_json:
#         return jsonify({'msg': 'Invalid request format'}), 400

#     email = request.json.get('email', None)
#     first_name = request.json.get('first_name', None)
#     last_name = request.json.get('last_name', None)
#     phone = request.json.get('phone', None)
#     password = request.json.get('password', None)
#     company_id = request.json.get('company_id', None)


@auth_bp.post('/register_invitee')
def invite():
    if not request.is_json:
        return jsonify({'msg': 'Invalid request format.'}), HTTPStatus.BAD_REQUEST

    email = request.json.get('email', None)
    invite_code = request.json.get('invite_code', None)
    password = request.json.get('password', None)

    if email is None or invite_code is None or password is None:
        return jsonify({'msg': 'Missing required fields.'}), HTTPStatus.BAD_REQUEST

    invitee = UserInvite.query.filter_by(email=email).first()

    # Check that the invitee exists
    if invitee is None:
        return jsonify({'msg': 'There is no invite for you yet.'}), HTTPStatus.NOT_FOUND

    # Check that the invitee has not already accepted the invite
    if invitee.has_accepted:
        return jsonify({'msg': 'You have already accepted the invite.'}), HTTPStatus.BAD_REQUEST

    # Check that request's invite code matches the invitee's invite code
    if invitee.invite_code is not invite_code:
        return jsonify({'msg': 'Invalid invite code.'}), HTTPStatus.UNAUTHORIZED

    password = bcrypt.generate_password_hash(password, 16).decode('utf-8')

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

    # Set the invitee's has_accepted field to True
    invitee.has_accepted = True

    db.session.commit()

    return jsonify({'msg': 'Successfully registered.'}), HTTPStatus.OK
