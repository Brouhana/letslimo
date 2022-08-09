from app import ma, db
from app.models.trip_groups import TripGroup


class TripGroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TripGroup
        sqla_session = db.session
        load_instance = True
        exclude = ('id', 'created_on', 'last_updated',)
