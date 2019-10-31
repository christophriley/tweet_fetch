import logging
import re

import pandas as pd
import spacy

from db import engine, Tweet
from gensim import corpora
from gensim.models import TfidfModel, LdaModel

# gensim prints to logs instead of stdout
logging.basicConfig(level=logging.INFO)

df = pd.read_sql_table(Tweet.__tablename__, engine)

#tokenize and remove stopwords
spacy_model = spacy.load("en", disabled=["ner", "parser", "tagger"])
def preprocess(text):
    result = []
    for token in spacy_model(text):
        if token.is_stop:
            continue
        if len(token.text) < 3:
            continue
        result.append(token.lower_)
    return result

preprocessed_tweets = [preprocess(tweet) for tweet in df.text]

dictionary = corpora.Dictionary(preprocessed_tweets)

corpus = [dictionary.doc2bow(tweet) for tweet in preprocessed_tweets]

tfidf = TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

lda = LdaModel(
    corpus_tfidf, 
    id2word=dictionary, 
    num_topics=5, 
    passes=20,
    alpha=.001,
)
corpus_lda = lda[corpus_tfidf]
lda.print_topics()