import requests

from auth import TwitterAuth

twitter_auth = TwitterAuth()
token = twitter_auth.get_bearer_token()
print(token)