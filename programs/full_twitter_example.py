
# coding: utf-8

# # Assignment 6

# In[1]:

#Zach King Predict420


# ### Objective

#Learn how to connect to social media network (we will use Twitter as example in this assignment), and collect/preprocess/analyze its data


#Tweets Data Can be used for different purposes by the candidates campaigns. Below is a sample list of examples where candidates twitter accounts and tweets can be used:
#    1. Use TwitterAPI in Python to view followers and friends for 2016 Presidential Candidates 
#    2. Use TwitterAPI in Python to view hot-topics and what can be trending among candidates and friends
#    3. Use TwitterAPI in Python to view what Sunday Talk Shows most followed by the candidates



#Candidates (republicans and democrates) have differents accounts on Twitter but does the number of Twitter followers equal number of supporters for the inidividual candidates?



#Which Presidential Candidate has Only 1,800 Twitter Followers?

#From 4 million to 1,800, the 2016 presidential candidates ranked by their Twitter followings. Read the following article to get an idea: 
#http://observer.com/2015/10/which-presidential-candidate-has-only-1800-twitter-followers/


# ### Installation and Setup
#For this assignment you need to do the following setup first:

#1.  Install  Python package  TwitterAPI. 
    pip install TwitterAPI

#2.  Create an account on twitter.com.

#3.  Generate authentication tokens by following the instructions here : 
#    https://dev.twitter.com/oauth/overview/application-owner-access-tokens

#4.  Add your tokens to the credentials.txt file.



# ### Twitter API
#Twitter API

#Two APIs:

#    REST API: Submit HTTP requests to access specific information (tweets, friends, ...)
#    Streaming API: Open a continuous connection to Twitter to receive real-time data.

#These APIs are  HTTP GET request


#Here are the twitter API docs that you must familiarize yourself with

#https://dev.twitter.com/rest/reference/get/followers/ids

#https://dev.twitter.com/overview/api/twitter-libraries

#When you search in a text (tweets are text messages), often you need to be aware of something STOP WORDS.
#You could read more about stop-words here:
 
#    https://en.wikipedia.org/wiki/Stop_words
    
# # Lets create twitter object and use its API. Code snippets below will show you how to use this API

# In[2]:

from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager


# In[3]:

o = TwitterOAuth.read_file('credentials.txt')


# In[4]:

o.access_token_key


# In[5]:

# Using OAuth1...
twitter = TwitterAPI(o.consumer_key,
                 o.consumer_secret,
                 o.access_token_key,
                 o.access_token_secret)


# In[6]:

help(twitter)


# In[7]:

# What can we do with this twitter object?
# builtin method `dir` tells us...
dir(twitter)


# In[8]:

twitter.auth


# In[9]:

# Get help on the `request` method using the builtin method called...`help`
help(twitter.request)


# In[1]:

# Let's start by querying the search API
response = twitter.request('search/tweets', {'a': 'big+data'}) 


# In[11]:

# What object is returned?
# builtin type method will tell us.
print type(response)
dir(response)


# In[12]:

response.json


# In[13]:

response.status_code
# See https://dev.twitter.com/overview/api/response-codes


# In[14]:

tweets = [r for r in response]


# In[15]:

print('found %d tweets' % len(tweets))


# In[16]:

type(tweets)


# In[17]:

type(tweets[0])


# In[18]:

tweets[0]


# In[19]:

help(tweets[0])


# In[20]:

tweets[0].keys()


# In[21]:

tweets[0]['text']


# In[22]:

tweets[0]['created_at']


# In[23]:

tweets[14]['text']


# In[24]:

tweets[0]['user']


# In[25]:

user = tweets[0]['user']
print('screen_name=%s, name=%s, location=%s' % (user['screen_name'], user['name'], user['location']))


# In[26]:

# Who follows this person?
# https://dev.twitter.com/docs/api/1.1/get/followers/list
screen_name = user['screen_name']
response  = twitter.request('followers/list', {'screen_name': screen_name, 'count':200})
followers = [follower for follower in response]
        
print 'found %d followers for %s' % (len(followers), screen_name)
# See more about paging here: https://dev.twitter.com/docs/working-with-timelines


# In[27]:

print followers[0]['screen_name']


# In[28]:

# Get this person's timeline
timeline = [tweet for tweet in twitter.request('statuses/user_timeline',
                                                {'screen_name': screen_name,
                                                 'count': 200})]
print 'got %d tweets for user %s' % (len(timeline), screen_name)


# In[29]:

# Print the text.
print '\n\n\n'.join(t['text'] for t in timeline)


# In[3]:

str(pb)


# In[30]:

# Count words
from collections import Counter  # This is just a fancy dict mapping from object->int, starting at 0.
counts = Counter()
for tweet in timeline:
    counts.update(tweet['text'].lower().split())
print('found %d unique terms in %d tweets' % (len(counts), len(timeline)))
counts.most_common(10)


# In[31]:

# Sort by value, descending.
# See more about Python's lambda expressions:
# https://docs.python.org/2/tutorial/controlflow.html#lambda-expressions

sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)



# In[32]:

print '\n'.join('%s=%d' % (term[0], term[1])  
                for term in sorted_counts[:10])


# # Now lets collect data about few of the 2016 presidential candidates

# In[33]:

#Create LOT (List-Of-Tuples) for 2016 Presidential Candidates

LOT_presidentialCandidates = [('HillaryClinton', 'D'), 
                              ('MartinOMalley', 'D'), 
                              ('BernieSanders', 'D'),
                              ('realDonaldTrump', 'R'),
                              ('JebBush', 'R'),
                              ('RealBenCarson', 'R'),
                              ('ScottWalker', 'R'),
                              ('CarlyFiorina', 'R'),
                              ('GovMikeHuckabee', 'R'),
                              ('DrRandPaul', 'R')]


# ### Lets see first HillaryClinton Friends We put a limit max 200 friends

# In[34]:

# Lets see first HillaryClinton Friends
# We put a limit max 200 friends


response = twitter.request('friends/list', {'screen_name': 'realDonaldTrump', 'count':200})
friends = [r for r in response]


# ### Lets see how many friends for every candidate. We put a limit max 200 friends

# In[35]:

candidatesFriends={}

for candidate in  LOT_presidentialCandidates:
    response = twitter.request('friends/list', {'screen_name': candidate[0], 'count':200})
    friends = [r for r in response]
    print candidate[0], '  has ', len(friends), ' friends'
    candidatesFriends[candidate[0]]=friends


# ###  Sanity test: lets see who are Trumps friends

# In[36]:

# Sanity test: lets see who are Trumps friends

for friend in candidatesFriends['HillaryClinton']:
    print friend['screen_name']


# ###  Who are the most popular friends by republicans (candidates)?

# In[37]:

# Who are the most popular friends by republican party?


# separate candidates by party.
republicans = [candidate[0] for candidate in LOT_presidentialCandidates if candidate[1] == 'R']
democrats = [candidate[0] for candidate in LOT_presidentialCandidates if candidate[1] == 'D']
print('%d republicans, %d democrats' % (len(republicans), len(democrats)))


print('popular Republican friends:')

republican_counts = Counter()

for candidate in  LOT_presidentialCandidates: 
    if candidate[0] in republicans:
        for friend in candidatesFriends[candidate[0]]:
            republican_counts[friend['screen_name']] += 1
 
print republican_counts.most_common(3)



# # Requirement #1: which friend is followed by the most number of candidates?

# In[38]:

friend_counts = Counter()
for candidate in  LOT_presidentialCandidates: 
    for friend in candidatesFriends[candidate[0]]:
            friend_counts[friend['screen_name']] += 1
 
print friend_counts.most_common(1)


# # Requirement #2: Get the top 10 list of popular Democrats(candidates) friends

# In[39]:

democrats = [candidate[0] for candidate in LOT_presidentialCandidates if candidate[1] == 'D']

print('popular Democrats friends:')

democrat_counts = Counter()

for candidate in  LOT_presidentialCandidates: 
    if candidate[0] in democrats:
        for friend in candidatesFriends[candidate[0]]:
            democrat_counts[friend['screen_name']] += 1
print democrat_counts.most_common(10)           


# In[ ]:



