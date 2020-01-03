import requests
import urllib.request
import time
from bs4 import BeautifulSoup

yogamag = 'http://yogamag.net'

response = requests.get(yogamag)
soup = BeautifulSoup(response.text, 'html.parser')

diccio = {}

# <option> del cercador de la pàgina principal

for idx, option in enumerate(soup.find_all('option')):
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
            # print('article: {}'.format(article))
        diccio[year] = article_list

# Pinto el diccionari --> any: llista d'articles d'aquell any
print(diccio)
