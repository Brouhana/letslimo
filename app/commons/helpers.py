from flask_jwt_extended import get_jwt


def can_access_company(company_id):
    return int(company_id) == get_jwt()['sub']['company_id']
