import json

from auth import TwitterAuth
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
    group.add_argument(
        '--limits',
        action='store_true',
        help='Print information about the current rate limits of the app'
    )
    args = parser.parse_args()

    if args.user:
        tweets = get_user_tweets(args.user)
        print(json.dumps(tweets, indent=2))
    elif args.mention:
        raise NotImplementedError
    elif args.limits:
        limits = TwitterAuth.get_limits()
        print(json.dumps(limits, indent=2))
