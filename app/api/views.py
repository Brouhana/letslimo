from flask import Blueprint

from app.api.resources.company.user import UserResource
from app.api.resources.company.company import CompanyResource
from app.api.resources.company.vehicle import VehicleResource
from app.api.resources.company.contacts_company import ContactsCompanyResource
from app.api.resources.company.contacts_customers import ContactsCustomerResource


api_bp = Blueprint('api', __name__, url_prefix='/api/company/')


user_view_func = UserResource.as_view('users')
company_view_func = CompanyResource.as_view('company')
vehicle_view_func = VehicleResource.as_view('vehicle')
contacts_company_view_func = ContactsCompanyResource.as_view(
    'contacts_company')
contacts_customer_view_func = ContactsCustomerResource.as_view(
    'contacts_customer')


api_bp.add_url_rule('/<int:company_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=company_view_func)

# /<int:company_id>/users/
api_bp.add_url_rule('/<int:company_id>/users',
                    methods=['GET', 'POST'],
                    defaults={'user_id': None},
                    view_func=user_view_func)
api_bp.add_url_rule('/<int:company_id>/users/<user_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=user_view_func)

# /<int:company_id>/vehicles
api_bp.add_url_rule('/<int:company_id>/vehicles',
                    methods=['GET', 'POST'],
                    defaults={'vehicle_id': None},
                    view_func=vehicle_view_func)
api_bp.add_url_rule('/<int:company_id>/vehicles/<vehicle_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=vehicle_view_func)

# /<int:company_id>/contacts/companies
api_bp.add_url_rule('/<int:company_id>/contacts/companies',
                    methods=['GET', 'POST'],
                    defaults={'contacts_company_id': None},
                    view_func=contacts_company_view_func)
api_bp.add_url_rule('/<int:company_id>/contacts/companies/<int:contacts_company_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=contacts_company_view_func)

# /<int:company_id>/contacts/customers
api_bp.add_url_rule('/<int:company_id>/contacts/customers',
                    methods=['GET', 'POST'],
                    defaults={'contacts_customer_id': None},
                    view_func=contacts_customer_view_func)
api_bp.add_url_rule('/<int:company_id>/contacts/customers/<int:contacts_customer_id>',
                    methods=['GET', 'PUT', 'DELETE'],
                    view_func=contacts_customer_view_func)
