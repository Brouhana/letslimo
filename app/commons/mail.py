import requests
import os
from app.commons.localdatetime import get_local_datetime

POSTMARK_EMAIL_API = "https://api.postmarkapp.com/email"
POSTMARK_EMAIL_TEMPLATE_API = "https://api.postmarkapp.com/email/withTemplate"
NO_REPLY_EMAIL = os.environ.get('NO-REPLY-EMAIL')

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Postmark-Server-Token': os.environ.get('POSTMARK_SERVER_TOKEN')
}


def send_reservation_conf(trip):
    to = trip.contacts_customer.email
    company_name = trip.company.company_name
    booking_contact_name = trip.contacts_customer.full_name
    vehicle = trip.vehicle.name
    trip_code = trip.trip_code_sub
    passenger = trip.passenger
    company_email = trip.company.company_booking_email
    company_phone = trip.company.company_phone
    company_address = trip.company.company_address

    if (trip.passenger is not None):
        passenger = trip.passenger['full_name']
    else:
        passenger = booking_contact_name

    # utc = pytz.timezone('UTC')
    # operator_tz = pytz.timezone(get_jwt()['sub']['timezone'])
    # utc_date = utc.localize(trip.pu_datetime)
    # utc_time = utc.localize(trip.pu_datetime)
    # operator_tz_date = operator_tz.normalize(utc_date.astimezone(operator_tz))
    # operator_tz_time = operator_tz.normalize(utc_time.astimezone(operator_tz))

    pu_date = get_local_datetime(trip.pu_datetime).strftime(
        "%m/%d/%Y"),
    pu_time = get_local_datetime(trip.pu_datetime).strftime(
        "%I:%M %p"),

    text = 'Your reservation for {} on {} at {} is below.'.format(
        vehicle, *pu_date, *pu_time)

    payload = {
        'From': '{} {}'.format(company_name, NO_REPLY_EMAIL),
        'To': to,
        'MessageStream': 'reservations',
        "TemplateAlias": 'operator-reservation-confirm',
        'TemplateModel': {
            'company_name': company_name,
            'company_email': company_email,
            'company_address': company_address,
            'company_phone': company_phone,
            'passenger_name': passenger,
            'text': text,
            'trip_code': trip_code,
            'booking_contact_name': booking_contact_name,
        }
    }

    response = requests.post(POSTMARK_EMAIL_TEMPLATE_API,
                             headers=headers, json=payload)

    return response.status_code, response.json()


def send_invite(to,
                invitee_first_name,
                invitee_last_name,
                inviter_full_name,
                company_name,
                invite_code,
                type):
    payload = {
        'From': '{} {}'.format(company_name, NO_REPLY_EMAIL),
        'To': to,
        'MessageStream': 'user-invites',
        "TemplateAlias": 'invite-driver-template' if type == 'driver' else 'invite-member-template',
        'TemplateModel': {
            'invitee_first_name': invitee_first_name,
            'invitee_last_name': invitee_last_name,
            'inviter_full_name': inviter_full_name,
            'company_name': company_name,
            'invite_code': invite_code,

        }
    }

    response = requests.post(POSTMARK_EMAIL_TEMPLATE_API,
                             headers=headers, json=payload)

    return response.status_code, response.json()
