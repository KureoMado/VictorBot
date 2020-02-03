import requests
import random
import time
from bs4 import BeautifulSoup as BS

def tavern_thread():
    href = 'STARTED'
    tavern = 'https://dota2.ru/forum/new/threads/'
    r = requests.get(tavern)
    html = BS(r.content, "lxml")
    for i in range(12):
        tav = html.find_all("div", {"class": "secondRow"})
        ad = tav[i]
        alist = ad.find_all('a')
        catl = alist[1]
        cat = catl.contents[0]
        divt = html.find_all("h3", {"class": "title"})
        d = divt[i]
        if cat != 'Таверна':
            continue
        else:
            break
    ainf = d.select('a')
    a = ainf[0]['href']
    href = 'https://dota2.ru/forum/' + str(a)
    return href
