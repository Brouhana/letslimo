from flask import Blueprint

from app.api.resources.company.user import UserResource
from app.api.resources.company.company import CompanyResource
from app.api.resources.company.vehicle import VehicleResource


api_bp = Blueprint('api', __name__, url_prefix='/api/company/')


user_view_func = UserResource.as_view('users')

api_bp.add_url_rule('/<int:company_id>/users',
                    methods=['GET', 'POST'],
                    defaults={'user_id': None},
                    view_func=user_view_func)
api_bp.add_url_rule('/<int:company_id>/users/<user_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=user_view_func)


company_view_func = CompanyResource.as_view('company')

api_bp.add_url_rule('/<int:company_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=company_view_func)


vehicle_view_func = VehicleResource.as_view('vehicle')

api_bp.add_url_rule('/<int:company_id>/vehicles',
                    methods=['GET', 'POST'],
                    defaults={'vehicle_id': None},
                    view_func=vehicle_view_func)
api_bp.add_url_rule('/<int:company_id>/vehicles/<vehicle_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=vehicle_view_func)
