#!/usr/bin/env python
# coding: utf-8

# Package imports
import itertools
import pandas as pd
import preprocessor as p
import re
import sklearn.feature_extraction
import string
import unidecode
from nltk.stem import PorterStemmer, LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
from langdetect import detect
import seaborn as sns
import spacy
import json
import sys

# Lambda function for printing
debug = lambda x: print(x)

debug("<<<Start>>>")

# Create punctuation removal variable
rm_punc = str.maketrans('', '', string.punctuation)

# Create stopword removal variable
stopwords = sklearn.feature_extraction.text.ENGLISH_STOP_WORDS
temp_word = set(stopwords)

 # Additional stopwords 
new_words_temp = []
with open('/Users/tomashegewisch/research_project/Tomas/data/add_stopwords.json') as f:
    new_words_temp = json.load(f)['stopwords']
for i in new_words_temp:
    temp_word.add(i)
stopwords = frozenset(temp_word)

# Create stemmer variables
porter = PorterStemmer()
lancaster = LancasterStemmer()

debug("<<<load the data>>>")
# Import JSON files containing tweet dataset(s)
path = str(sys.argv[1])
try:
    tweets = pd.read_json(path, lines=True, orient='record')
except:
    print("The path was not found")

#tweets = tweets.head(1000)

# View all rows contained in the dataset(s)
pd.set_option('display.max_rows', tweets.shape[0]+1)

debug("<<<duplicates>>>")
# Check for duplicate tweets
debug("BEFORE")
debug(len(tweets))
tweets.drop_duplicates(subset=['id'], keep="first", inplace=True)
debug("\nAFTER")
debug(len(tweets))

debug("<<<Remove non-englisch>>>")
# Remove all tweets which are not English
def language(text):
    try:
        return detect(text)
    except:
        return "en"
    
debug(len(tweets))
tweets = tweets[tweets['tweet'].apply(language) == "en"]
debug(len(tweets))


# Stopword and link removal
def remove_stopwords(word):
    if word in stopwords:
        return ''
    if word.startswith('http') or word.startswith('pictwittercom') or word.endswith('com') or word.endswith('coza'):
        return ''
    return word

# Preprocessing the tweet
def preprocess(text):
    clean_data = []
    for x in text:
        new_text = re.sub('<.*?>', '', x)   # remove HTML tags
        new_text = re.sub(r'[^\w\s]', '', new_text) # remove punctuation
        new_text = re.sub(r'\d+','',new_text) # remove numbers
        new_text = re.sub('\n', ' ', new_text) #remove escape characters
        new_text = new_text.lower() # lower case         
        if new_text != '':
            clean_data.append(new_text)
        temp_string = ''
        for i in clean_data:
            temp_string += i
    clean_data = temp_string
    return clean_data

# Cleaning and tokenising the tweet
def clean_tweet(tweet):
    tweet = preprocess(tweet)
    tweet = unidecode.unidecode(tweet).lower().split()
    tweet = [remove_stopwords(x) for x in tweet]
    tweet = list(itertools.chain.from_iterable([x.split() for x in tweet if x != '']))
    tweet = [x for x in tweet if len(x) > 1]
    return tweet

def make_clean_text(tweet): 
    # pre-processing package.
    return p.clean(tweet)

debug("<<<First apply function>>>")
tweets['tokenised'] = tweets['tweet'].apply(clean_tweet)

debug("<<<Secound apply function>>>")
tweets['tweet_clean'] = tweets['tweet'].apply(make_clean_text)

debug("<<Remove>>")



def find_non_text(text):
    if text == []:
        return "NA"
debug("<<<drop non-words>>>")

#DROP rows that do not have text in them...
debug("Before")
debug(len(tweets))
tweets = tweets[tweets['tokenised'].apply(find_non_text) != "NA"]
debug("After")
debug(len(tweets))

debug("<<<send to pkl>>>")
tweets.to_pickle("/Users/tomashegewisch/Desktop/all_6_months_2.pkl")