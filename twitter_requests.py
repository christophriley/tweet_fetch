import logging
import os
import requests

from auth import TwitterAuth

log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOG_LEVEL', 'WARNING'))

SEARCH_ENDPOINT_KEY = '/search/tweets'

endpoints = {
    SEARCH_ENDPOINT_KEY: 'https://api.twitter.com/1.1/search/tweets.json',
}

auth = TwitterAuth()

def _send_request(endpoint_key, params={}):
    url = endpoints.get(endpoint_key)
    auth.decrement_limit(endpoint_key)
    headers = {
        'Authorization': 'Bearer ' + auth.bearer_token
    }

    log.info('Sending request to %s' % url)
    r = requests.get(url, params=params, headers=headers)
    return r.json()

def get_user_tweets(user_name):
    params = {
        'count': 100,
        'q': f"from:{user_name}"
    }
    return _send_request(SEARCH_ENDPOINT_KEY, params=params)