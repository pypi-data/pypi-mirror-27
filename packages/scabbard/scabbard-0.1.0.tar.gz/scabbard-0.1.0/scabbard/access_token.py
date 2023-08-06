import json
import requests
import base64
from datetime import datetime, timedelta
import iso8601
import pytz
import logging

token_cache_file_path = 'cached_access_token.json'


class ExpiredTokenException(Exception):
    pass


def b64(to_encode):
    return base64.b64encode(to_encode.encode('utf-8')).decode("utf-8")


def get_token():
    # check cached access_token
    try:
        with open(token_cache_file_path, 'r') as ataj:
            cached_token_from_file = json.loads(ataj.read())
        cache_expiration_timestamp_utc = iso8601.parse_date(cached_token_from_file['expiration_date'])
        utc_time_now = pytz.utc.localize(datetime.utcnow())
        # check to see if the cached token will expire in less than an hour from now
        expired = utc_time_now > cache_expiration_timestamp_utc - timedelta(hours=1)
        if expired:
            raise ExpiredTokenException()
        # return cached token
        logging.info('using cached access token')
        return cached_token_from_file['access_token']
    except (FileNotFoundError, ExpiredTokenException):
        logging.info('getting new access token')
        # get new token and save cached copy for subsequent requests
        with open('api_connection_parameters.json', 'r+') as cpf:
            config = json.loads(cpf.read())
        credentials = (config["formatVersion"] + ":"
                       + config["clientId"] + ":"
                       + config["group"] + ":"
                       + config["domain"])
        secret = b64(config["clientSecret"])
        credentials = b64(b64(credentials) + ":" + secret)

        headers = {
            'Authorization': "Basic " + credentials,
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(config["environment"] + "/v2/auth/token", headers=headers,
                                 data={"grant_type": "client_credentials"})

        objresponse = json.loads(response.text)
        objresponse['expiration_date'] = (pytz.utc.localize(datetime.utcnow()) +
                                          timedelta(seconds=objresponse['expires_in']))
        token_cache_content = {
            'expiration_date': objresponse['expiration_date'].isoformat(),
            'access_token': objresponse['access_token']
        }

        # overwrite file with latest access token
        with open(token_cache_file_path, 'w') as ataj:
            ataj.write(json.dumps(token_cache_content, sort_keys=True, indent=4))

        return token_cache_content['access_token']


if __name__ == "__main__":
    # get access_token
    token = get_token()
    print(token)
