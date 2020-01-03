import requests
import urllib.request
import time
from bs4 import BeautifulSoup

yogamag = 'http://yogamag.net'
healthandyoga = 'https://www.healthandyoga.com/html/newsinfo.aspx'

response = requests.get(healthandyoga)
soup = BeautifulSoup(response.text, 'html.parser')

# <option> del cercador de la pàgina principal
diccio = {}

for idx, l in enumerate(soup.find_all('li')):
    # print('IDX: {}\n{}'.format(idx, l))
    if idx == 8:                # idx 8 és el que té els tipus d'articles de yoga
        links = soup.find_all('a')
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

                diccio[tipologia] = article_list

# # Pinto el diccionari --> antipologia: llista d'articles d'aquella tipologia
print(diccio)
