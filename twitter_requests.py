import logging
import os
import requests

from urllib.parse import parse_qs
from auth import TwitterAuth

log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOG_LEVEL', 'WARNING'))

SEARCH_ENDPOINT_KEY = '/search/tweets'
TIMELINE_ENDPOINT_KEY = '/statuses/user_timeline'
SEARCH_COUNT = 100
TIMELINE_COUNT = 200

endpoints = {
    SEARCH_ENDPOINT_KEY: 'https://api.twitter.com/1.1/search/tweets.json',
    TIMELINE_ENDPOINT_KEY: 'https://api.twitter.com/1.1/statuses/user_timeline.json'
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

def _get_lowest_id(tweets):
    """Return the lowest (i.e. least recent) id from a collection of tweets"""
    lowest_id = None
    for tweet in tweets:
        tweet_id = tweet.get('id')
        if lowest_id is None or tweet_id < lowest_id:
            lowest_id = tweet_id
    return lowest_id

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

def _get_user_tweets_batch(user_name, max_id=None):
    """Get the next batch of tweets for a user, using the next_results parameter to set the 
    max_id if it is given"""
    log.info('Retrieving tweets from %s with %s' %(user_name, max_id))
    params = {
        'count': TIMELINE_COUNT,
        'screen_name': user_name,
    }

    if max_id is not None:
        params['max_id'] = max_id
    
    tweets = _send_request(TIMELINE_ENDPOINT_KEY, params=params)
    log.info('Retrieved %d tweets' % len(tweets))
    
    lowest_id = _get_lowest_id(tweets)
    return tweets, lowest_id

def get_user_tweets(user_name):
    """Retrieve all (accessible) tweets from a given user name by stepping backward through the status paging"""
    all_tweets, lowest_id = _get_user_tweets_batch(user_name)
    while True:
        next_batch, lowest_id = _get_user_tweets_batch(user_name, lowest_id)
        all_tweets += next_batch
        
        # The list of tweets may include the one with the given max_id, so 
        # we need to use <= instead of strict <
        if len(next_batch) <= 1:
            break
    return all_tweets
    