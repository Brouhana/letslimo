from flask_jwt_extended import get_jwt
import pytz


def get_local_datetime(dt):
    utc = pytz.timezone('UTC')
    user_tz = pytz.timezone(get_jwt()['sub']['timezone'])
    utc_datetime = utc.localize(dt)
    return user_tz.normalize(utc_datetime.astimezone(user_tz))
