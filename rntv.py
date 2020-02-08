import requests
import random
from bs4 import BeautifulSoup as BS
from datetime import datetime

now = datetime.today()

def date_pars(pdate):
    date_result = 0
    mnths_list = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 'Jule' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}
    pd = int(pdate[0:2])
    pm = int(mnths_list[pdate[3:6]])
    py = int(pdate[7:11])
    post_date = datetime(py, pm, pd)
    period = now - post_date
    datedelta = int(period.days)
    if datedelta <= 2:
        date_result = 1
    else:
        date_result = 0
    return date_result

def mat_search():
    #ПОИСК
    BAD_WORDS = ['бля', 'сука', 'хер', 'херня', 'дохера', 'нихера', 'нахер', 'похер', 'нахера', 'нихуя' 'хуйня', 'похуй', 'долбоеб', 'хохол', 'чурка', 'хач']
    READY_LIST = []
    for i in range(len(BAD_WORDS)):
        link = 'https://dota2.ru/forum/search?type=post&keywords='+ BAD_WORDS[i] + '&users=&date=&nodes%5B%5D=all'  # составление запроса
        r = requests.get(link)
        html = BS(r.content, "lxml")
        div_search = html.find_all("h3", {"class": "title"}) #выборка дивов с контентом
        post_date_raw = html.find_all("abbr", {"class": "date-time"})
        cat_chk = html.find_all("div", {"class": "meta"})
        if div_search != 0:
            for dsc in range(len(div_search)):
                try:
                    pdate = str(post_date_raw[dsc]['title'])
                    delta = date_pars(pdate)
                    if delta == 1:
                        cat_n = cat_chk[dsc]
                        get_cat = cat_n.select('a')
                        category = get_cat[1].text
                        cat_list = [
                        'Таверна', 'Творчество', 'Музыка',
                        'Кино и сериалы', 'Аниме и прочее', 'Спорт',
                        'Книги', 'Другие игры', 'Консольные игры',
                        'League of Legends', 'MMO', 'Path of Exile',
                        'Shooter', 'Battle Royale', 'ККИ, Автобаттлеры',
                        'Hearthstone', 'Artifact', 'Dota Underlords'
                        ]
                        if str(category) in cat_list:
                            div = div_search[dsc]
                            to_check = div.select('a')
                            a = to_check[0]['href']
                            violation = BAD_WORDS[i]
                            f_link = 'Возможное нарушение: ' + str(violation) + '\nhttps://dota2.ru/forum/' + str(a)
                            READY_LIST.append(f_link)
                    i += 1
                except:
                    i += 1
    return READY_LIST

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
