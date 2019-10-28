# tweet_fetch
Simple module for fetching tweets from the Twitter public API

## Configuring
Fill out the consumer key and consumer secret values in `sample_credentials.py` and rename it to `credentials.py`. These secret credentials can be found on your [Twitter Developer App Page] (https://developer.twitter.com/en/apps).

## Usage
Install requirements.
```bash
$ pip install -r requirements.txt
```

Set the log level if you want to get information on what the script is doing
```bash
$ export LOG_LEVEL=INFO
```

Run the script with the `--user` option to retrieve a user's timeline. 

```bash
$ python tweet_fetch.py --user twitterapi
INFO:auth:Current remaining limit for /statuses/retweeters/ids is 300
INFO:auth:Current remaining limit for /statuses/show/:id is 900
INFO:auth:Current remaining limit for /statuses/user_timeline is 1482
INFO:auth:Current remaining limit for /statuses/retweets/:id is 300
INFO:auth:Current remaining limit for /statuses/oembed is 180
INFO:auth:Current remaining limit for /statuses/lookup is 300
INFO:auth:Current remaining limit for /search/tweets is 450
INFO:twitter_requests:Retrieving tweets from twitterapi with None
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 426418815212060672
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 195182242128080896
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 199 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 113996333848866816
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 198 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 78883323421786112
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 60784492436140032
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 34654128231821312
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 28739639595
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 22028354286
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 17387588253
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 12965082418
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 199 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 10033937399
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 6773185286
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 4658672683
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 2541614876
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 2035638160
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 200 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 1780328154
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 57 tweets
INFO:twitter_requests:Retrieving tweets from twitterapi with 1740144322
INFO:twitter_requests:Sending request to https://api.twitter.com/1.1/statuses/user_timeline.json
INFO:twitter_requests:Retrieved 1 tweets
INFO:db:Saving 3254 tweets to database
```
