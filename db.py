import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Boolean, String, Enum, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker

import logging, os
log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOG_LEVEL', 'WARNING'))

engine = create_engine('sqlite:///tweet_data.db')
Session = sessionmaker(bind=engine)


Base = declarative_base()

class EntityType(enum.Enum):
    hashtag = 1
    mention = 2

class Tweet(Base):
    """Stores Tweets themselves"""
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    user = Column(String, index=True)
    text = Column(Text)
    truncated = Column(Boolean)
    is_retweet = Column(Boolean)
    reply_to = Column(String)

    def __repr__(self):
        return ("ID: %d\n"
                "<Truncated>\n" if self.truncated else ""
                "%s") % (self.id, self.text)

class TweetEntity(Base):
    """Associates Tweet ids with hashtags or mentions they contain"""
    __tablename__ = 'tweet_entity'

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    type = Column(Enum(EntityType), index=True)
    value = Column(String, index=True)


Base.metadata.create_all(engine)

def save_tweets(tweets_json):
    log.info("Saving %d tweets to database" % len(tweets_json))
    session = Session()
    for tweet_json in tweets_json:
        new_tweet = Tweet(
            id = tweet_json.get('id'),
            user = tweet_json.get('user').get('screen_name'),
            truncated = tweet_json.get('truncated'),
            text = tweet_json.get('text', tweet_json.get('full_text')),
            is_retweet = tweet_json.get('retweeted_status') is not None,
            reply_to = tweet_json.get('in_reply_to_screen_name'),
        )
        session.merge(new_tweet)

        entities = tweet_json.get('entities')
        for hashtag in entities.get('hashtags'):
            new_entity = TweetEntity(
                tweet_id = tweet_json.get('id'),
                type = EntityType.hashtag,
                value = hashtag.get('text'),
            )
            session.merge(new_entity)
        
        for user_mention in entities.get('user_mentions'):
            new_entity = TweetEntity(
                tweet_id = tweet_json.get('id'),
                type = EntityType.mention,
                value = user_mention.get('screen_name'),
            )
            session.merge(new_entity)

    session.commit()
