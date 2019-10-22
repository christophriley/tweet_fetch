from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Boolean, create_engine
from sqlalchemy.orm import sessionmaker

import logging, os
log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOG_LEVEL', 'WARNING'))

engine = create_engine('sqlite:///tweet_data.db')
Session = sessionmaker(bind=engine)


Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    truncated = Column(Boolean)

    def __repr__(self):
        return ("ID: %d\n"
                "<Truncated>\n" if self.truncated else ""
                "%s") % (self.id, self.text)

Base.metadata.create_all(engine)

def save_tweets(tweets_json):
    log.info("Saving %d tweets to database" % len(tweets_json))
    session = Session()
    for tweet_json in tweets_json:
        new_tweet = Tweet(
            id = tweet_json.get('id'),
            truncated = tweet_json.get('truncated'),
            text = tweet_json.get('text')
        )
        session.merge(new_tweet)
    session.commit()
