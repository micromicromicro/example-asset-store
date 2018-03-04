import json
import smtplib
import os
from email.mime.text import MIMEText

import boto3
import boto3.session

s3 = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'))

store_email = os.environ['SEND_EMAIL']
store_email_server = os.environ['SEND_EMAIL_SERVER']
store_email_port = os.environ['SEND_EMAIL_PORT']
store_email_starttls = os.environ['SEND_EMAIL_STARTTLS'] == '1'
store_email_user = os.environ['SEND_EMAIL_USERNAME']
store_email_pw = os.environ['SEND_EMAIL_PASSWORD']
token = os.environ['SEND_TOKEN']
store_bucket = os.environ['SEND_BUCKET']


def handler(event, context=0, callback=0):
    if event.get('queryStringParameters', {}).get('t') != token:
        return dict(
            statusCode=403,
            body='Bad token',
        )
    data = json.loads(event['body'])
    if 'testing' in data:
        return dict(statusCode=200, body='')
    message = json.loads(data['message'])
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params=dict(
            Bucket=store_bucket,
            Key=message['id'],
        ),
        ExpiresIn=24 * 60 * 60,
    )
    msg = MIMEText(
        _text='Download {} here: {}'.format(message['name'], url),
        _charset='utf-8'
    )
    msg['Subject'] = 'Your download link for {} from My Asset Store'.format(
        message['name'])
    msg['From'] = 'My Asset Store <{}>'.format(store_email)
    msg['To'] = message['email']
    with smtplib.SMTP(store_email_server, store_email_port) as s:
        if store_email_starttls:
            s.starttls()
        s.login(store_email_user, store_email_pw)
        s.sendmail(store_email, [msg['To']], msg.as_string())
    return dict(
        statusCode=200,
        body='',
    )
