from flask import Blueprint

from app.api.resources.operator.users.user import UserResource
from app.api.resources.operator.companies.company import CompanyResource
from app.api.resources.operator.vehicles.vehicle import VehicleResource
from app.api.resources.operator.contacts.contacts_company import ContactsCompanyResource
from app.api.resources.operator.contacts.contacts_customers import ContactsCustomerResource
from app.api.resources.operator.trips.trip import TripResource
from app.api.resources.operator.invoices.invoice import InvoiceResource


api_operator_bp = Blueprint(
    'api', __name__, url_prefix='/api/operator/company/')


user_view_func = UserResource.as_view('users')
company_view_func = CompanyResource.as_view('company')
vehicle_view_func = VehicleResource.as_view('vehicle')
contacts_company_view_func = ContactsCompanyResource.as_view(
    'contacts_company')
contacts_customer_view_func = ContactsCustomerResource.as_view(
    'contacts_customer')
trip_view_func = TripResource.as_view('trip')
invoice_view_func = InvoiceResource.as_view('invoice')


api_operator_bp.add_url_rule('/<int:company_id>',
                             methods=['GET', 'PUT', 'DELETE'],
                             view_func=company_view_func)

# /<int:company_id>/users/
api_operator_bp.add_url_rule('/<int:company_id>/users',
                             methods=['GET', 'POST'],
                             defaults={'user_id': None},
                             view_func=user_view_func)
api_operator_bp.add_url_rule('/<int:company_id>/users/<user_id>',
                             methods=['GET', 'PUT', 'DELETE'],
                             view_func=user_view_func)

# /<int:company_id>/vehicles
api_operator_bp.add_url_rule('/<int:company_id>/vehicles',
                             methods=['GET', 'POST'],
                             defaults={'vehicle_id': None},
                             view_func=vehicle_view_func)
api_operator_bp.add_url_rule('/<int:company_id>/vehicles/<vehicle_id>',
                             methods=['GET', 'PUT', 'DELETE'],
                             view_func=vehicle_view_func)

# /<int:company_id>/contacts/companies
api_operator_bp.add_url_rule('/<int:company_id>/contacts/companies',
                             methods=['GET', 'POST'],
                             defaults={'contacts_company_id': None},
                             view_func=contacts_company_view_func)
api_operator_bp.add_url_rule('/<int:company_id>/contacts/companies/<int:contacts_company_id>',
                             methods=['GET', 'PUT', 'DELETE'],
                             view_func=contacts_company_view_func)

# /<int:company_id>/contacts/customers
api_operator_bp.add_url_rule('/<int:company_id>/contacts/customers',
                             methods=['GET', 'POST'],
                             defaults={'contacts_customer_id': None},
                             view_func=contacts_customer_view_func)
api_operator_bp.add_url_rule('/<int:company_id>/contacts/customers/<int:contacts_customer_id>',
                             methods=['GET', 'PUT', 'DELETE'],
                             view_func=contacts_customer_view_func)


# /<int:company_id>/trips
api_operator_bp.add_url_rule('/<int:company_id>/trips',
                             methods=['GET', 'POST'],
                             defaults={'trip_id': None},
                             view_func=trip_view_func)
api_operator_bp.add_url_rule('/<int:company_id>/trips/<int:trip_id>',
                             methods=['GET', 'PUT', 'DELETE'],
                             view_func=trip_view_func)


# /<int:company_id>/invoices
api_operator_bp.add_url_rule('/<int:company_id>/invoices',
                             methods=['GET', 'POST'],
                             defaults={'invoice_id': None},
                             view_func=invoice_view_func)
api_operator_bp.add_url_rule('/<int:company_id>/invoices/<int:invoice_id>',
                             methods=['GET', 'PUT', 'DELETE'],
                             view_func=invoice_view_func)
