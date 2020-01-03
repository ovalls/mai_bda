# -*- coding: utf-8 -*-
from __future__ import division
from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import operator
import nltk

# Establish connection with database
client = MongoClient()
db = client.test
col = db.twitter_bda_yoga

#######################################################
# Retrieve data from the mongodb database, choosing
# the fields you'll need afterwards						-- collection: twitter_bda_yoga
#######################################################

my_tweets = db.twitter_bda_yoga.find({},{'lang':1, '_id':0, 'text':1, 'entities.hashtags':1,
'in_reply_to_status_id':1, 'is_quote_status':1, 'retweeted_status':1, 'user.followers_count':1,
'user.screen_name':1, 'retweet_count':1})

numTweets = db.twitter_bda_yoga.estimated_document_count()

print('- Num Tweets captured:\n  {}'.format(numTweets))

print('- First 20 captured tweets:')
for t in range(0, 20):
	print('  {}'.format(my_tweets[t]))


###################################################################
# Plot of Languages (autodetected by Twitter) for the first hashtag
###################################################################

langsList = []
for t in my_tweets:
	langsList.append(t['lang'])

D = Counter(langsList)
print('- Languages:\n  {}'.format(D))
#print('- values:\n{}'.format(D.values()))

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

originals_percent = round(originals*100/numTweets,2)
replies_percent = round(replies*100/numTweets,2)
quotations_percent = round(quotations*100/numTweets,2)
retweets_percent = round(retweets*100/numTweets,2)

print('- Content generated via (number of tweets, from a total number of {}:'.format(numTweets))
print('  Original: {} ({}%)'.format(originals, originals_percent))
print('  Replies: {} ({}%)'.format(replies, replies_percent))
print('  Quotations: {} ({}%)'.format(quotations, quotations_percent))
print('  Retweets: {} ({}%)'.format(retweets, retweets_percent))

# ----------- Pie Chart ------------------------------------
sizes = [originals, retweets, quotations, replies]
labels = 'Original Content', 'Retweets', 'Quotations', 'Replies'
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
#frequencies = [x/numTweets for x in sizes]
explode = (0.1, 0, 0, 0)  # explode 1st slice
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
		autopct='%1.2f%%', shadow=True, startangle=140)
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

#print('- dictionary:\n{}'.format(dict_followers))
sorted_dict = sorted(dict_followers.items(), key=operator.itemgetter(1), reverse=True) #ordena de + a - (reverse)
#print('- sorted_dict:\n{}'.format(sorted_dict))

# I get the first 20 users with more followers
first20 = list(sorted_dict)[0:20]
print('- Top 20 users by followers\' number:\n  {}'.format(first20))

# ----------- Horizontal Bar Plot ------------------------
pos = range(len(first20))
#reverse list to the able to print the higher numbers up
first20 = list(reversed(first20))
plt.barh(pos, [val[1] for val in first20], align ='center', color ='lightskyblue') # + a dalt - a baix
plt.yticks(pos, [val[0] for val in first20])
plt.title('Top 20 users captured with the highest number of followers')
plt.tight_layout()
plt.show()


##################################################################
# Plot secondary hashtags
##################################################################
my_tweets.rewind()
hashList = []
for t in my_tweets:
	for e in t['entities']['hashtags']:
		h = e['text']
		#print('h: {}'.format(h))
		if h.lower() != 'yoga':
			hashList.append(h.lower())

D = Counter(hashList)
subset = dict(D.most_common(30))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))
reversed_list = sorted_subset[::-1]
print('- Top 30 of secondary hashtags:\n  {}'.format(reversed_list))

# ----------- Horizontal Bar Plot ------------------------
pos = range(len(sorted_subset))
plt.barh(pos, [val[1] for val in sorted_subset], align = 'center', color = 'blue')
plt.yticks(pos, [val[0] for val in sorted_subset])
plt.title('Top 30 of secondary hashtags captured (apart from yoga')
plt.tight_layout()
plt.show()


##################################################################
# What's inside the texts?
##################################################################
my_tweets.rewind()
hashList = []

for t in my_tweets:
	if t['lang'] == 'en':
		words = []
		words.append(t['text'].split())
		#print('words: {}'.format(words))
		for w in words[0]:  # guarda les paraules en llista d'una llista de paraules words = [['ds','rr',...]]
			if w.startswith('@') or w.startswith('#'):
				w = w[1:]
			if w.endswith(':'):
				w = w[0:len(w)-1]
			if len(w) > 3 and w[-1] == '.' and w[-2] == '.' and w[-3] == '.':	# acaba en ...
				w = w[0:len(w)-3]
			if w.lower() != 'yoga':
				hashList.append(w.lower())

# em quedo amb les paraules que són noms (NLTK)
ptags = []
for h in hashList:
	#print('h: {}'.format(h))
	if h != '' and len(h) > 2 and h[0] != '&':
		pt = nltk.pos_tag([h])
		if pt[0][1][0] in 'N':
			#print('pt: {}'.format(pt))
			if 'http' not in h:
				ptags.append(h)

#print('POS-TAGs:\n{}'.format(ptags))

D = Counter(ptags)
subset = dict(D.most_common(50))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))
reversed_list = sorted_subset[::-1]
print('- 50 most common words in twitter texts:\n  {}'.format(reversed_list))

subset1 = sorted_subset[0:25]
subset2 = sorted_subset[25:100]

# ----------- Horizontal Bar Plot (first 25) ------------------------
pos = range(len(subset1))
plt.barh(pos, [val[1] for val in subset1], align = 'center', color = 'yellowgreen') # + a dalt - a baix
plt.yticks(pos, [val[0] for val in subset1])
plt.title('Top 25 most common words from text of tweets captured in english')
plt.tight_layout()
plt.show()
# ----------- Horizontal Bar Plot (next 25) ------------------------
pos = range(len(subset2))
plt.barh(pos, [val[1] for val in subset2], align = 'center', color = 'yellowgreen') # + a dalt - a baix
plt.yticks(pos, [val[0] for val in subset2])
plt.title('Second pack of 25 most common words from text of tweets captured in english')
plt.tight_layout()
plt.show()

