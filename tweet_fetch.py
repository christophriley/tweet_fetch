import json

from auth import TwitterAuth
from db import save_tweets
import twitter_requests

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Use the Twitter public API to retrieve tweets for use in datasets')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--user',
        help='Retrieve tweets made by the given handle'
    )
    group.add_argument(
        '--search',
        help='Search for tweets with the given query'
    )
    args = parser.parse_args()

    if args.user:
        tweets = twitter_requests.get_user_tweets(args.user)
        save_tweets(tweets)
    elif args.search:
        tweets = twitter_requests.search(args.search)
        save_tweets(tweets)