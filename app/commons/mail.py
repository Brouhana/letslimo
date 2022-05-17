import requests
import os

POSTMARK_API = 'https://api.postmarkapp.com/email'
FROM_EMAIL = 'brennan@letslimo.com'


def send_mail(to_email, subject, html_body):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Postmark-Server-Token': os.environ.get('POSTMARK_SERVER_TOKEN')
    }
    payload = {
        'From': FROM_EMAIL,
        'To': to_email,
        'Subject': subject,
        'Htmlbody': html_body,
        'MessageStream': 'user-invites'
    }

    response = requests.post(POSTMARK_API, headers=headers, json=payload)

    return response.status_code, response.json()
