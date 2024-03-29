# From https://developer.twitter.com/en/docs/basics/authentication/overview/application-only
# The steps to encode an application’s consumer key and secret into a set of credentials to obtain a bearer token are:

#     URL encode the consumer key and the consumer secret according to RFC 1738. Note that at the time of writing, this will not actually change the consumer key and secret, but this step should still be performed in case the format of those values changes in the future.
#     Concatenate the encoded consumer key, a colon character ”:”, and the encoded consumer secret into a single string.
#     Base64 encode the string from the previous step.
import base64
import logging
import os
import requests
import urllib.parse
import time

from credentials import credentials

log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOG_LEVEL', 'WARNING'))


AUTH_ENDPOINT = 'https://api.twitter.com/oauth2/token'
AUTH_REQUEST_BODY = 'grant_type=client_credentials'
AUTH_CONTENT_TYPE = 'application/x-www-form-urlencoded;charset=UTF-8'
RESPONSE_TOKEN_KEY = 'access_token'

LIMIT_ENDPOINT ='https://api.twitter.com/1.1/application/rate_limit_status.json'

class TwitterAuth:
    def __init__(self):
        self.limits = {}
        # Encode according to RFC 1738, which does nothing at the time of this writing but
        # may do something in the future
        key = urllib.parse.quote(credentials.get('consumer_key'))
        secret = urllib.parse.quote(credentials.get('consumer_secret'))
        
        # Concatenate key and secret with an intervening colon
        joined = key + ":" + secret

        # Base64 encode the concatenated string to use as the basic authoriziation key
        self.encoded_key = base64.b64encode(joined.encode()).decode()

        headers = {
            'Authorization': 'Basic ' + self.encoded_key,
            'Content-Type': AUTH_CONTENT_TYPE
        }

        r = requests.post(AUTH_ENDPOINT, data=AUTH_REQUEST_BODY, headers=headers)
        self.bearer_token = r.json().get(RESPONSE_TOKEN_KEY)
        logging.info('Successfully authenticated')
        self.refresh_limits()

    def refresh_limits(self):
        headers = {
            'Authorization': 'Bearer ' + self.bearer_token
        }
        params = {
            'resources': 'search,statuses'
        }
        r = requests.get(LIMIT_ENDPOINT, headers=headers, params=params)
        limit_groups = r.json().get('resources')
        for limit_group in limit_groups.values():
            for key, limit_object in limit_group.items():
                limit_value = limit_object.get('remaining')
                self.limits[key] = limit_value
                log.info('Current remaining limit for %s is %d' % (key, limit_value))

    def decrement_limit(self, key):
        current_limit = self.limits[key]
        if current_limit <= 0:
            log.warning('Rate limit reached for %s. Sleeping for 15 minutes' % key)
            time.sleep(15 * 60)
            self.refresh_limits()
            current_limit = self.limits[key]
            log.warning('Resuming with new limit of %d' % current_limit)
        
        new_limit = current_limit - 1
        if new_limit % 50 == 0:
            log.info('Limit for %s is now at %d' % (key, new_limit))
        self.limits[key] = new_limit