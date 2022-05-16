from flask import jsonify
from flask_jwt_extended import get_jwt
from http import HTTPStatus


def can_access_company(company_id: int):
    return int(company_id) == get_jwt()['sub']['company_id']
