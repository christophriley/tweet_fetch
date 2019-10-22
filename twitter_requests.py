import os
import requests

from auth import TwitterAuth

import logging
log_level = os.environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=log_level)

SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'


def _send_request(endpoint, params={}):
    token = TwitterAuth.get_bearer_token()
    headers = {
        'Authorization': 'Bearer ' + token
    }

    r = requests.get(endpoint, params=params, headers=headers)
    return r.json()

def get_user_tweets(user_name):
    params = {
        'count': 100,
        'q': f"from:{user_name}"
    }
    return _send_request(SEARCH_URL, params=params)