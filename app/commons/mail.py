import requests
import os

POSTMARK_EMAIL_API = "https://api.postmarkapp.com/email"
POSTMARK_EMAIL_TEMPLATE_API = "https://api.postmarkapp.com/email/withTemplate"
NO_REPLY_EMAIL = os.environ.get('NO-REPLY-EMAIL')


def send_invite(to,
                invitee_first_name,
                invitee_last_name,
                inviter_full_name,
                company_name,
                invite_code,
                type):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Postmark-Server-Token': os.environ.get('POSTMARK_SERVER_TOKEN')
    }
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
