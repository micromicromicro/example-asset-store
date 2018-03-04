import json
import datetime
import os

from botocore.vendored import requests

micromicro_username = os.environ['MM_USERNAME']
micromicro_token = os.environ['MM_TOKEN']

# The price is in 1 / 100 litecoin minimum denomination.
# Prices can be specified in other currencies by getting the exchange rate
# when creating the in address.
assets = {
    'asset1.txt': dict(
        name='Asset 1',
        price=10000000,
    ),
    'asset2.txt': dict(
        name='Asset 2',
        price=17000000,
    )
}


def handler(event, context=0, callback=0):
    data = json.loads(event['body'])
    asset = assets.get(data['id'])
    if not asset:
        raise RuntimeError('Unknown asset {}'.format(data['id']))
    resp = requests.post(
        'https://api.development.micromicro.cash/v1/new_in',
        json=dict(
            # micromicro username
            username=micromicro_username,

            # micromicro login token - you can see this by logging into micromicro
            # and checking local storage, key `config`, child key `token`
            token=micromicro_token,

            # You can also specify a specific TOS version - then the api will stop
            # working if a new TOS is released without your approval
            tos='latest',

            # We don't need the received money to usable quickly, save money this
            # way
            slow=True,

            # This could be true or false, but it may prevent people from
            # accidentally double purchasing if they're absent minded.
            single_use=True,

            # The purchase must be made within 24h.  This prevents unused addresses
            # from accumulating.
            expire=int(
                (
                    datetime.datetime.utcnow() + datetime.timedelta(days=1)
                ).timestamp() * 1000
            ),

            # This data will be sent to our webhook endpoint
            receiver_message=json.dumps(dict(
                name=asset['name'],
                id=data['id'],
                email=data['email'],
            )),

            amount=asset['price'],

            # Default text for the user's transaction record
            sender_message='Buy {} from My Asset Store'.format(asset['name']),
        )
    )
    resp.raise_for_status()
    resp = resp.json()
    return dict(
        statusCode=200,
        headers={
            'Access-Control-Allow-Origin' : '*',
        },
        body=str(resp['id']),
    )
