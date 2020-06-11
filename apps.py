import requests
import psycopg2
import random
from bs4 import BeautifulSoup as BS
from datetime import datetime
import config

now = datetime.today()

#DATE CHECK
def date_pars(pdate):
    date_result = 0
    mnths_list = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}
    post_date = datetime(int(pdate[7:11]), int(mnths_list[pdate[3:6]]), int(pdate[0:2]))
    datedelta = int((now - post_date).days)
    if datedelta <= 2:
        date_result = 1
    else:
        date_result = 0
    return date_result

#VIOLATIONS
def d2ru_violations(d2ru_category):
    #ПОИСК
    BAD_WORDS = BAD_WORDS = ['сука', 'сучк*', 'хер', 'херн*', '*хера', '*ахер*', 'похер*', '*хуй*', '*пизд*', 'долбоеб*','*аху*', 'ебат*', 'выеб*', 'уеб*', 'съеб*'] #СПИСОК СЛОВ
    CATEGORIES = {
    'Разное' : ['Таверна', 'Творчество', 'Музыка', 'Кино и сериалы', 'Аниме и прочее', 'Спорт', 'Книги', 'Другие игры',
                'Консольные игры', 'League of Legends', 'MMO', 'Path of Exile', 'Shooter, Battle Royale', 'Valorant', 'ККИ, Автобаттлеры',
                'Hearthstone', 'Artifact', 'Dota Underlords'],
    'Основа' : ['Общие вопросы и обсуждения', 'Обитель нытья', 'Dota Plus, компендиумы и ивенты', 'Обновления и патчи',
                'Рейтинговая система и статистика', 'Герои: общие обсуждения', 'Dream Dota', 'Нестандартные сборки',
                'Киберспорт: общие обсуждения', 'Игроки и команды', 'Турниры, матчи и прогнозы',
                'Поиск игроков для ммр и паб игр', 'Поиск игроков для создания команды',
                'Поиск команды для совместных игр и участия в турнирах', 'Поиск игроков для ивентов и абузов',
                'Обмен предметами и гифтами', 'Обсуждения и цены', 'Медиа Dota 2', 'Стримы', 'Развитие портала']
    }
    RAW_LIST = [] #список без исключений
    #Цикл для проверки по каждому слову из BAD_WORDS
    for i in range(len(BAD_WORDS)):
        link = 'https://dota2.ru/forum/search?type=post&keywords='+ BAD_WORDS[i] + '&users=&date=&nodes%5B%5D=all'  # составление запроса
        r = requests.get(link)
        html = BS(r.content, "lxml")
        div_search = html.find_all("h3", {"class": "title"}) #дивы с постом
        post_date_raw = html.find_all("abbr", {"class": "date-time"}) #поиск элемента с датой поста
        cat_chk = html.find_all("div", {"class": "meta"}) #поиск элемента с именем раздела

        #Цикл для проверки по каждому посту на странице
        if div_search != 0:
            for dsc in range(len(div_search)):
                if date_pars(str(post_date_raw[dsc]['title'])) == 1:
                    #проверка раздела
                    get_cat = cat_chk[dsc].select('a')
                    cat_list = CATEGORIES[d2ru_category]
                    if str(get_cat[1].text) in cat_list:
                        #оформление сообщения
                        div = div_search[dsc]
                        f_link = 'Возможное нарушение: **' + str(BAD_WORDS[i]) + '**\nhttps://dota2.ru/forum/' + str(div.select('a')[0]['href'])
                        RAW_LIST.append(f_link)
        #Проверка на исключения
        READY_LIST = post_exc(RAW_LIST)

    return READY_LIST

#Запись в БД
def db_write(post_id):
    conn = psycopg2.connect(dbname=config.database, user=config.db_user, password=config.password, host=config.host)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO violation_ex (Violation) VALUES ('{0}')".format(post_id))
    conn.commit()
    cursor.close()
    conn.close()

#чек
def post_exc(raw):
    conn = psycopg2.connect(dbname=config.database, user=config.db_user, password=config.password, host=config.host)
    cursor = conn.cursor()
    cursor.execute("SELECT Violation FROM violation_ex;")
    rlist = []
    for row in cursor:
        rlist.append(str(row)[2:-3])
    cursor.close()
    conn.close()
    result = []
    for i in range(len(raw)):
        if raw[i][-9:-1] in rlist:
            pass
        else:
            result.append(raw[i])
    return result

def covid():
    countries = ['russia/','ukraine/','belarus/','kazakhstan/']
    covid_list = []
    #WORLD
    r = requests.get('https://www.worldometers.info/coronavirus/')
    html = BS(r.content, "lxml")
    wcs = html.find_all("div", {"class": "maincounter-number"}) #дивы с постом
    for i in range(3):
        wcr = wcs[i].select('span')[0].text.replace(',', ' ')
        covid_list.append(wcr)
    #COUNTRIES
    for i in range(len(countries)):
        r = requests.get('https://www.worldometers.info/coronavirus/country/' + str(countries[i]))
        html = BS(r.content, "lxml")
        wcs = html.find_all("div", {"class": "maincounter-number"}) #дивы с постом
        for n in range(3):
            wcr = wcs[n].select('span')[0].text.replace(',', ' ')
            covid_list.append(wcr)
    return covid_list
