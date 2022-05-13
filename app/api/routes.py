from flask import Blueprint
from app.api.resources.user import UserResource


api = Blueprint('api', __name__, url_prefix='/api/')

users_view_func = UserResource.as_view('users')

api.add_url_rule(
    '/users', methods=['GET'], defaults={'user_id': None}, view_func=users_view_func)
api.add_url_rule(
    '/users', methods=['POST'], view_func=users_view_func)
api.add_url_rule(
    '/users/<user_id>', methods=['GET', 'PUT', 'DELETE'], view_func=users_view_func)
