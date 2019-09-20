# From https://developer.twitter.com/en/docs/basics/authentication/overview/application-only
# The steps to encode an application’s consumer key and secret into a set of credentials to obtain a bearer token are:

#     URL encode the consumer key and the consumer secret according to RFC 1738. Note that at the time of writing, this will not actually change the consumer key and secret, but this step should still be performed in case the format of those values changes in the future.
#     Concatenate the encoded consumer key, a colon character ”:”, and the encoded consumer secret into a single string.
#     Base64 encode the string from the previous step.
import base64
import requests
import urllib.parse

from credentials import credentials


AUTH_ENDPOINT = 'https://api.twitter.com/oauth2/token'
AUTH_REQUEST_BODY = 'grant_type=client_credentials'
AUTH_CONTENT_TYPE = 'application/x-www-form-urlencoded;charset=UTF-8'
RESPONSE_TOKEN_KEY = 'access_token'

class TwitterAuth:
    def __init__(self):
        self.bearer_token = None
        
        # Encode according to RFC 1738, which does nothing at the time of this writing but
        # may do something in the future
        key = urllib.parse.quote(credentials.get('consumer_key'))
        secret = urllib.parse.quote(credentials.get('consumer_secret'))
        
        # Concatenate key and secret with an intervening colon
        joined = key + ":" + secret

        # Base64 encode the concatenated string to use as the basic authoriziation key
        self.encoded_key = base64.b64encode(joined.encode()).decode()

    def _retrieve_bearer_token(self):
        """Use the encoded key to request a bearer token from the auth endpoint"""
        headers = {
            'Authorization': 'Basic ' + self.encoded_key,
            'Content-Type': AUTH_CONTENT_TYPE
        }

        r = requests.post(AUTH_ENDPOINT, data=AUTH_REQUEST_BODY, headers=headers)
        self.bearer_token = r.json().get(RESPONSE_TOKEN_KEY)

    def get_bearer_token(self):
        if self.bearer_token is None:
            self._retrieve_bearer_token()
        return self.bearer_token