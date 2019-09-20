class TwitterRequest:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.additional_params = None

    def send(self, args):
        r = requests.post(AUTH_ENDPOINT, data=AUTH_REQUEST_BODY, headers=headers)

class SearchRequest(TwitterRequest):
    def __init__(self):
        search_url = 'https://api.twitter.com/1.1/search/tweets.json'
        super().__init__(search_url)