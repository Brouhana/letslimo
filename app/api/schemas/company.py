from app.models.company import Company
from app import ma


class CompanySchema(ma.Schema):
    class Meta:
        model = Company
