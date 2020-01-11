import requests
#import urllib.request
#import time
from bs4 import BeautifulSoup
from collections import Counter
import operator
import nltk
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

#######################################################################################################
# Websites with ARTICLES

yogamag = 'http://yogamag.net'
healthandyoga = 'https://www.healthandyoga.com/html/newsinfo.aspx'


#######################################################################################################
# Analize ARTICLES

#################################
######## www.yogamag.net ########
#################################

diccio_yogamag = {}
list_yogamag = []
articles_yogamag = 0

response_yogamag = requests.get(yogamag)
soup_yogamag = BeautifulSoup(response_yogamag.text, 'html.parser')

# <option> del cercador de la pàgina principal
for idx, option in enumerate(soup_yogamag.find_all('option')):
	site = option['value']
	year = option.text
	# print('\nvalue: {}, text: {}'.format(valor, texte))
	if idx > 2:
		# print('\nYEAR: {}, url articles: {}'.format(year, site))
		response = requests.get(yogamag + site)
		soup = BeautifulSoup(response.text, 'html.parser')
		h4s = soup.find_all('h4')
		article_list = []
		for h in h4s:
			article = h.text
			# alguns articles tenen \n, ho intento treure per quedar-me només amb el nom i no amb l'autor.
			article = article.split('\n')[0]    # ara ja tinc només els títols dels articles
			article_list.append(article)
			list_yogamag.append(article)
			# print('article: {}'.format(article))
			articles_yogamag += 1
		diccio_yogamag[year] = article_list

# Pinto el diccionari --> any: llista d'articles d'aquell any
print('\nDICTIONARY yogamag ({} articles)\n{}'.format(articles_yogamag, diccio_yogamag))
# Pinto la llista de títols d'articles
#print('\nLIST yogamag\n{}'.format(list_yogamag))

#hich on waves and editorial són temes que surten a cada revista -- ignorar dels resultats!!
D = Counter(list_yogamag)
subset = dict(D.most_common(50))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))
reversed_list = sorted_subset[::-1]
print('\n50 most common articles in yogamag website ({} articles):\n{}'.format(articles_yogamag, reversed_list))

#How many articals were published each year
dict_years = {}
for k,v in diccio_yogamag.items():
	dict_years[k] = len(v)
print('dict_years: \n{}'.format(dict_years))

# ----------- Bar Plot ------------------------
plt.bar(range(len(dict_years)), list(dict_years.values()), align='center')
plt.xticks(range(len(dict_years)), dict_years.keys(), rotation=45)
plt.title('Number of articles published per year')
plt.show()


#################################
##### www.healthandyoga.com #####
#################################

diccio_health = {}
list_health = []
articles_health = 0

response_health = requests.get(healthandyoga)
soup_health = BeautifulSoup(response_health.text, 'html.parser')

# <option> del cercador de la pàgina principal
for idx, l in enumerate(soup_health.find_all('li')):
	# print('IDX: {}\n{}'.format(idx, l))
	if idx == 8:                # idx 8 és el que té els tipus d'articles de yoga
		links = soup_health.find_all('a')
		# print(links)
		for idx2, l2 in enumerate(links):
			if idx2 > 22 and idx2 < 34:     # tipologies d'articles entre el 23 i el 33
				article_list = []           # llista d'articles de la tipologia

				tipologia = l2.text
				tipologia = " ".join(tipologia.title().split())       # treure espais de més
				site = l2.attrs['href']
				# print('\nIDX: {}\nTipologia: {}\nhref: {}'.format(idx2, tipologia, site))
				response = requests.get('https://www.healthandyoga.com' + site)
				soup = BeautifulSoup(response.text, 'html.parser')

				bodyLK = soup.findAll('a', {'class': 'bodyLK'})
				bodyLK.append(soup.find('a', {'class': 'bodyLk'}))

				# for idx3, blk in enumerate(soup.findAll('a', {'class': 'bodyLK'})):
				for idx3, blk in enumerate(bodyLK):
					# print('BLK: {}'.format(blk))
					if blk is not None:
						# els primers comencen per ../ i no són articles i els que el texte posa click tampoc
						if blk.attrs['href'][0] != '.' and 'Clicking' not in blk.text:
							text_blk = blk.text
							text_blk = " ".join(text_blk.title().split())       # treure espais de més
							site_blk = blk.attrs['href']
							# print('bodylk:\n{}'.format(bodylk))
							# print('   * idx: {}\n     Text: {}\n     url: {}'.format(idx3, text_blk, site_blk))
							article_list.append(text_blk)
							list_health.append(text_blk)
							articles_health += 1

				diccio_health[tipologia] = article_list

# Pinto el diccionari --> antipologia: llista d'articles d'aquella tipologia
print('\nDICTIONARY health and yoga (from {} articles)\n{}'.format(articles_health, diccio_health))
# Pinto la llista de títols d'articles
#print('\nLIST www.healthandyoga.com\n{}'.format(list_health))

D = Counter(list_health)
subset = dict(D.most_common(50))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))
reversed_list = sorted_subset[::-1]
print('\n50 most common articles in health and yoga website (from {} articles):\n{}'.
	  format(articles_health, reversed_list))

#How many articals were published per topic
dict_topics = {}
for k,v in diccio_health.items():
	dict_topics[k] = len(v)
print('dict_topics: \n{}'.format(dict_topics))

# ----------- Bar Plot ------------------------
plt.bar(range(len(dict_topics)), list(dict_topics.values()), align='center')
plt.xticks(range(len(dict_topics)), dict_topics.keys(), rotation=45)
plt.tight_layout()
plt.title('Number of articles published per topic')
plt.show()


#######################################################
# JOIN two dictionaries of articles (lists of articles)
#######################################################

#Jo faria un frequency bag de paraules d aquestes webs                              !!!!!!!!!!!!!!!!!!!
# i despres creuaria aquestes amb els hastags de twitter, per exemple....
articles = list_yogamag + list_health

D = Counter(articles)
subset = dict(D.most_common(50))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))
reversed_list = sorted_subset[::-1]
print('\n50 Most popular articles from both websites (from {} articles):\n{}'.
	  format(articles_yogamag+articles_health, reversed_list))


#######################################################################################################
# Analize WORDS on titles of all articles

#########################################
############ www.yogamag.net ############
#########################################

###tokens de cada títol d'article per poder quedar-me amb les paraules i mirar la freqüència

tokens_yogamag = []

for a in list_yogamag:
	tokens = word_tokenize(a.lower())
	for t in tokens:
		tokens_yogamag.append(t)

#print('\nTOKENS yogamag:\n{}'.format(tokens_yogamag))

# em quedo amb les paraules que són noms (pos-tags NLTK)
ptags = []
for h in tokens_yogamag:
	if h != '' and len(h) > 2 and h[0] != '&':
		pt = nltk.pos_tag([h])
		if pt[0][1][0] in 'N':
			#print('pt: {}'.format(pt))
			if 'http' not in h and 'waves' not in h and 'yoga' not in h and 'editorial' not in h:
				ptags.append(h)

D = Counter(ptags)
subset = dict(D.most_common(20))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))
reversed_list = sorted_subset[::-1]
print('\n20 most common words in yogamag articles (from {} articles):\n{}'.format(articles_yogamag, reversed_list))

# ----------- Horizontal Bar Plot ------------------------
pos = range(len(sorted_subset))
plt.barh(pos, [val[1] for val in sorted_subset], align ='center', color ='yellowgreen') # + a dalt - a baix
plt.yticks(pos, [val[0] for val in sorted_subset])
plt.title('20 most common nouns in yogamag articles')
plt.tight_layout()
plt.show()

#########################################
######### www.healthandyoga.com #########
#########################################

tokens_health = []

for a in list_health:
	tokens = word_tokenize(a.lower())
	for t in tokens:
		tokens_health.append(t)

#print('\nTOKENS health and yoga:\n{}'.format(tokens_health))

# em quedo amb les paraules que són noms (NLTK)
ptags = []
for h in tokens_health:
	#print('h: {}'.format(h))
	if h != '' and len(h) > 2 and h[0] != '&':
		pt = nltk.pos_tag([h])
		if pt[0][1][0] in 'N':
			#print('pt: {}'.format(pt))
			if 'http' not in h and 'yoga' not in h:
				ptags.append(h)

D = Counter(ptags)
subset = dict(D.most_common(20))
sorted_subset = sorted(subset.items(), key=operator.itemgetter(1))
reversed_list = sorted_subset[::-1]
print('\n20 most common words in health and yoga articles (from {} articles):\n{}'.
	  format(articles_health, reversed_list))

# ----------- Horizontal Bar Plot ------------------------
pos = range(len(sorted_subset))
plt.barh(pos, [val[1] for val in sorted_subset], align ='center', color ='yellowgreen') # + a dalt - a baix
plt.yticks(pos, [val[0] for val in sorted_subset])
plt.title('20 most common nouns in health and yoga articles')
plt.tight_layout()
plt.show()

###############################
# JOIN words from both websites
###############################

tokens_yoga = tokens_yogamag + tokens_health

# em quedo amb les paraules que són noms (NLTK)
ptags = []
for h in tokens_yoga:
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
print('\n50 most common words in all yoga articles (from {} articles):\n{}'.
	  format(articles_yogamag+articles_health, reversed_list))

