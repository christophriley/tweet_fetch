import json

from auth import TwitterAuth
from db import save_tweets
from twitter_requests import get_user_tweets

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Use the Twitter public API to retrieve tweets for use in datasets')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--user',
        help='Retrieve tweets made by the given handle'
    )
    group.add_argument(
        '--mention',
        help='Retrieve tweets mentioning the given handle'
    )
    args = parser.parse_args()

    if args.user:
        tweets = get_user_tweets(args.user)
        save_tweets(tweets.get('statuses'))
    elif args.mention:
        raise NotImplementedError