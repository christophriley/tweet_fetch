import logging
import os
import requests

from urllib.parse import parse_qs
from auth import TwitterAuth

log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOG_LEVEL', 'WARNING'))

SEARCH_ENDPOINT_KEY = '/search/tweets'
BATCH_COUNT = 100

endpoints = {
    SEARCH_ENDPOINT_KEY: 'https://api.twitter.com/1.1/search/tweets.json',
}

auth = TwitterAuth()

def _parse_search_results(json_result):
    """Search results are divided into 'statuses' and 'search_metadata'. The former
    contains the tweets themselves, and the latter contains the max_id to use to retrieve
    the next batch of tweets"""
    statuses = json_result.get('statuses')
    metadata = json_result.get('search_metadata')
    next_results = metadata.get('next_results')
    return statuses, next_results


def _send_request(endpoint_key, params={}):
    """Send the request to the Twitter API, keeping track of the rate limit and pausing if necessary"""
    url = endpoints.get(endpoint_key)
    auth.decrement_limit(endpoint_key)
    headers = {
        'Authorization': 'Bearer ' + auth.bearer_token
    }

    log.info('Sending request to %s' % url)
    r = requests.get(url, params=params, headers=headers)
    return r.json()

def _get_user_tweets_batch(user_name, next_results=None):
    """Get the next batch of tweets for a user, using the next_results parameter to set the 
    max_id if it is given"""
    log.info('Retrieving tweets from %s with %s' %(user_name, next_results))
    params = {
        'count': BATCH_COUNT,
        'q': f"from:{user_name}"
    }

    if next_results is not None:
        next_results = next_results.lstrip('?')
        next_results_parsed = parse_qs(next_results)
        params['max_id'] = next_results_parsed.get('max_id')[0]
    
    json_result = _send_request(SEARCH_ENDPOINT_KEY, params=params)
    statuses, next_results = _parse_search_results(json_result)
    log.info('Retrieved %d tweets' % len(statuses))
    return statuses, next_results

def get_user_tweets(user_name):
    """Retrieve all (accessible) tweets from a given user name by stepping backward through the status paging"""
    all_tweets, next_results = _get_user_tweets_batch(user_name)
    while True:
        next_batch, next_results = _get_user_tweets_batch(user_name, next_results)
        all_tweets += next_batch
        if len(next_batch) < 1:
            break
    return all_tweets
    