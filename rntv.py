import requests
import random
from bs4 import BeautifulSoup as BS

def random_thread():
    tavern = 'https://dota2.ru/forum/forums/taverna.6/'
    r = requests.get(tavern)
    html = BS(r.content, "lxml")
    div = html.find_all("div", {"class": "titleText"})
    th = div[random.randint(4,29)]
    a = th.select('a')
    a_th = a[0]['href']
    rhref = "https://dota2.ru/forum/" + a_th
    return rhref
