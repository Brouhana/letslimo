import requests
import os

POSTMARK_EMAIL_API = "https://api.postmarkapp.com/email"
POSTMARK_EMAIL_TEMPLATE_API = "https://api.postmarkapp.com/email/withTemplate"
NO_REPLY_EMAIL = os.environ.get('NO-REPLY-EMAIL')

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Postmark-Server-Token': os.environ.get('POSTMARK_SERVER_TOKEN')
}


def send_reservation_conf(to,
                          company_name,
                          booking_contact_name,
                          vehicle,
                          pu_date,
                          pu_time,
                          passenger_name,
                          company_email,
                          company_phone,
                          company_address):
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
            'passenger_name': passenger_name,
            'pu_time': pu_time,
            'pu_date': pu_date,
            'vehicle': vehicle,
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
