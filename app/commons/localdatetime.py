from flask_jwt_extended import get_jwt
import pytz
import datetime


def get_local_datetime(dt):
    utc = pytz.timezone('UTC')
    user_tz = pytz.timezone(get_jwt()['sub']['timezone'])
    utc_datetime = utc.localize(dt)
    return user_tz.normalize(utc_datetime.astimezone(user_tz))


def tz_diff_hours():
    """
    Returns difference hours between timezones
    """
    user_tz = get_jwt()['sub']['timezone']

    def is_dst():
        x = datetime.datetime(datetime.datetime.now().year, 1, 1, 0, 0, 0,
                              tzinfo=pytz.timezone(user_tz))
        y = datetime.datetime.now(pytz.timezone(user_tz))
        return not (y.utcoffset() == x.utcoffset())

    print(is_dst())

    # timezone = pytz.timezone(user_tz)
    # aware1 = timezone.localize(naive)
    # return offset_hours
