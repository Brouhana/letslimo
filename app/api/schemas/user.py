from app import ma
from app.models.user import User
from app.api.schemas.company import CompanySchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('password',)

    company = ma.Nested(CompanySchema)
