# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import operator

# Establish connection with database
client = MongoClient()
db = client.test
col = db.twitter_bda

#######################################################
# Retrieve data from the mongodb database, choosing
# the fields you'll need afterwards						-- collection: twitter_bda
#######################################################
my_tweets = db.twitter_bda.find({},{'lang':1, '_id':0, 'text':1, 'entities.hashtags':1,
'in_reply_to_status_id':1, 'is_quote_status':1, 'retweeted_status':1, 'user.followers_count':1,
'user.screen_name':1, 'retweet_count':1})
#retweet_count: Number of times this Tweet has been retweeted.

numTweets = db.twitter_bda.estimated_document_count()

print('- numTweets:\n{}'.format(numTweets))

print('- my_tweets:')
for t in range(0,19):
	print(my_tweets[t])


###################################################################
# Plot of Languages (autodetected by Twitter) for the first hashtag
###################################################################
'''
langsList = []
for t in my_tweets:
	langsList.append(t['lang'])

D = Counter(langsList)
print('- languages:\n{}'.format(D))
print('- values:\n{}'.format(D.values()))

# ----------- Bar Plot ------------------------
plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), D.keys())
plt.title('Languages spoken in the tweets captured')
plt.show()
'''
langsList = []
for t in my_tweets:
	langsList.append(t['lang'])

D = Counter(langsList)
print('- languages:\n{}'.format(D))
print('- values:\n{}'.format(D.values()))

# ----------- Bar Plot ------------------------
plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), D.keys())
plt.title('Languages spoken in the tweets captured')
plt.show()

##############################################################
# Plot how many of them are retweets, replies,
# quotations or original tweets
##############################################################
my_tweets.rewind() #Reset cursor
retweets = 0
replies = 0
quotations = 0
originals = 0
for t in my_tweets:
	if t.get('retweeted_status') is not None:
		retweets = retweets+1
	elif t['is_quote_status'] is not False:
		quotations = quotations+1
	elif t.get('in_reply_to_status_id') is not None:
		replies = replies+1
	else:
		originals = originals+1

# ----------- Pie Chart ------------------------
sizes = [originals, retweets, quotations, replies]
labels = 'Original Content', 'Retweets', 'Quotations', 'Replies'
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
#frequencies = [x/numTweets for x in sizes]
explode = (0.1, 0, 0, 0)  # explode 1st slice
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
		autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('Percentage of Tweets depending on how the content is generated')
plt.show()


########################################################
# Plot Top 20 users with the highest number of followers
########################################################
my_tweets.rewind()
dict_followers = {}
for t in my_tweets:
	u = t['user']['screen_name']
	f = t['user']['followers_count']
	dict_followers[u] = f

print('- dictionary:\n{}'.format(dict_followers))

sorted_dict = sorted(dict_followers.items(), key=operator.itemgetter(1), reverse=True) #ordena de + a - (reverse)
print('- sorted_dict:\n{}'.format(sorted_dict))

# I get the first 15 users with more followers
first20 = list(sorted_dict)[0:20]
print('First 20: {}'.format(first20))

# ----------- Horizontal Bar Plot ------------------------
pos = range(len(first20))
#reverse list to the able to print the higher numbers up
first20 = list(reversed(first20))
plt.barh(pos, [val[1] for val in first20], align ='center', color ='lightskyblue') # + a dalt - a baix
plt.yticks(pos, [val[0] for val in first20])
plt.title('Top 20 users captured with the highest number of followers')
plt.tight_layout()
plt.show()


###########################################################
# Top 20 hashtags for climatic, ecologic and organic issues
###########################################################
my_tweets.rewind() #Reset cursor
hashList = []
word1 = 'clima'		#clima, climate...
word2 = 'ecol'		#ecologie, ecologic, ecológico...
word3 = 'organic'

for t in my_tweets:
	for e in t['entities']['hashtags']:
		h = e['text']
		if word1 in h.lower() or word2 in h.lower() or word3 in h.lower():
			hashList.append(h)
D = Counter(hashList)

subset = dict(D.most_common(20))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))

print('20 climate/weather: {}'.format(sorted_subset))

# ----------- Horizontal Bar Plot ------------------------
pos = range(len(sorted_subset))
plt.barh(pos, [val[1] for val in sorted_subset], align = 'center', color = 'yellowgreen') # + a dalt - a baix
plt.yticks(pos, [val[0] for val in sorted_subset])
plt.title('Top 20 hashtags for climatic, ecologic and organic issues')
plt.tight_layout()
plt.show()


