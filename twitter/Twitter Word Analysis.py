# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 13:23:18 2016

@author: weizeng
"""

import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data_path = '/Users/weizeng/Documents/twitter_analysis/vr_removeps.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
print len(tweets_data)

tweets = pd.DataFrame(tweets_data)


tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

import re

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

k1 = tweets.loc[(tweets['lang'] =="en")]



k1['game'] = k1['text'].apply(lambda tweet: word_in_text('game', tweet))
k1['vr'] = k1['text'].apply(lambda tweet: word_in_text('vr', tweet))

import nltk  # draw on the Python natural language toolkit
from nltk.corpus import PlaintextCorpusReader
import sklearn.feature_extraction.text as text

my_additional_stop_words=['http','www','https','img','ff','href','says',
'import','make','february',
'com','january',]
stop_words = text.ENGLISH_STOP_WORDS.union(my_additional_stop_words)
s=set(stop_words)
    
word=[]

for tweet in tweets_data:
    tweet_text=tweet['text']
    tweet_text=tweet_text.encode('utf-8')
    tweet_text=tweet_text.rstrip('_:/\|><@_#$"&%*^()'+"'"+'')
    tweet_text=tweet_text.replace("\n", "")
    tweet_text=tweet_text.replace("\t", "")
    tweet_text=tweet_text.lower()
    m=tweet_text.split()
    #print m
    for w in m:
        if re.search('/x+',w) or re.search('\xd0',w) or re.search('\xe3',w) or re.search('https',w):
            continue
        else:
            word.append(w)
        
        
filtered_word_list = word[:] #make a copy of the word_list
for w in word: # iterate over word_list
  if w in s: 
    filtered_word_list.remove(w)
word_dict={}
for w in filtered_word_list: 
    if w in word_dict:
        word_dict[w]+=1
    else: 
        word_dict[w]=1
newdict={}    
for m in word_dict:
    if word_dict[m]==1:
        continue
    else:
        newdict[m]=word_dict[m]
        
import operator
m=sorted(newdict.items(),key=operator.itemgetter(1),reverse=True)
     
tdm_method=text.CountVectorizer(max_features=50, stop_words=stop_words)
examine_tdm_method=tdm_method.fit(filtered_word_list)
top_30_words=examine_tdm_method.get_feature_names()
top_30_words
print (map(lambda t: t.encode('ascii'), top_30_words)) #this part doesn't work 
    
