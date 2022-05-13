from flask import Blueprint

from app.api.resources.user import UserResource
from app.api.resources.company import CompanyResource


api_bp = Blueprint('api', __name__, url_prefix='/api/')

user_view_func = UserResource.as_view('users')
company_view_func = CompanyResource.as_view('companies')

api_bp.add_url_rule('/users',
                    methods=['GET'],
                    defaults={'user_id': None},
                    view_func=user_view_func)
api_bp.add_url_rule('/users',
                    methods=['POST'],
                    view_func=user_view_func)
api_bp.add_url_rule('/users/<user_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=user_view_func)

api_bp.add_url_rule('/companies/<company_id>',
                    methods=['GET', 'PUT'],
                    view_func=company_view_func)
