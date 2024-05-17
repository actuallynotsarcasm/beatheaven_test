import json
import requests_oauthlib


def get_request_token():
    callback_url = 'http://localhost:3000'

    with open('creds_discogs.json', 'r') as f:
        credentials = json.load(f)

    session_request = requests_oauthlib.OAuth1Session(
        client_key=credentials['consumer_key'],
        client_secret=credentials['consumer_secret'],
        callback_uri=callback_url
    )

    token_resp = session_request.fetch_request_token('https://api.discogs.com/oauth/request_token')

    with open('request_token_discogs.json', 'w') as f:
        f.write(json.dumps(token_resp, indent=4))

    print(f'https://discogs.com/oauth/authorize?oauth_token={token_resp['oauth_token']}')


def get_access_token():
    callback_url = 'http://localhost:3000'

    with open('creds_discogs.json', 'r') as f:
        credentials = json.load(f)
    with open('request_token_discogs.json', 'r') as f:
        request_token = json.load(f)

    session_access = requests_oauthlib.OAuth1Session(
        client_key=credentials['consumer_key'],
        client_secret=credentials['consumer_secret'],
        resource_owner_key=request_token['oauth_token'],
        resource_owner_secret=request_token['oauth_token_secret'],
        callback_uri=callback_url,
        verifier=request_token['oauth_verifier']
    )

    token_resp = session_access.fetch_access_token('https://api.discogs.com/oauth/access_token')

    with open('access_token_discogs.json', 'w') as f:
        f.write(json.dumps(token_resp, indent=4))


get_access_token()