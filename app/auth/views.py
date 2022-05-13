from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_bcrypt import check_password_hash

from app.models.user_operator import OperatorUser


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.post('/login')
def login():
    """
    Authenticates a user's credentials and returns tokens
    """

    if not request.is_json:
        return jsonify({"msg": "Invalid request format"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"msg": "Email or password is empty."}), 400

    user = OperatorUser.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({"msg": "Incorrect email or password."}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    res = {"access_token": access_token, "refresh_token": refresh_token}

    return jsonify(res), 200
