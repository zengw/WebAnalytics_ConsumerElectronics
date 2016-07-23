
# coding: utf-8

# In[1]:

from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager


# In[2]:

o = TwitterOAuth.read_file('credentials.txt')


# In[4]:

twitter = TwitterAPI(o.consumer_key,
                 o.consumer_secret,
                 o.access_token_key,
                 o.access_token_secret)


# In[5]:

twitter.auth


# In[83]:

response = twitter.request('search/tweets', {'q': 'perfect+beer','count': 100}) 


# In[84]:

tweets = [r for r in response]


# In[85]:

print('found %d tweets' % len(tweets))


# In[102]:

tweets[15]['text']


# In[106]:

timeline = [tweet for tweet in tweets]
print 'got %d tweets' % (len(timeline))
from collections import Counter
counts = Counter()
for tweet in timeline:
    counts.update(tweet['text'].lower().split())
print('found %d unique terms in %d tweets' % (len(counts), len(timeline)))


# In[103]:

sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)


# In[105]:

print '\n'.join('%s=%d' % (term[0], term[1])  
                for term in sorted_counts[:100])


# In[130]:

print '\n\n\n'.join(t['text'] for t in timeline)


# In[137]:

print '\n\n\n'.join(t['text'] for t in timeline).encode('utf-8').strip()


# In[138]:

text_file = open("perfect_beer_tweets.txt", "w")
print >>  text_file, '\n\n\n'.join(t['text'] for t in timeline).encode('utf-8').strip()
text_file.close()


# In[ ]:



