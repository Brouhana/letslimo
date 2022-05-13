from app import ma


class CompanySchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'is_active',
            'company_name',
            'company_address',
            'company_website_url',
            'company_general_email',
            'company_booking_email',
            'company_phone',
            'created_on',
            'last_updated',
        )
