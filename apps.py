import requests
import random
from bs4 import BeautifulSoup as BS
from datetime import datetime

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
    BAD_WORDS = ['сука', 'хер', 'херн*', '*хера', '*ахер*', 'похер*', '*хуй*', '*пизд*', 'долбоеб*'] #СПИСКО СЛОВ
    CATEGORIES = {
    'Разное' : ['Таверна', 'Творчество', 'Музыка', 'Кино и сериалы', 'Аниме и прочее', 'Спорт', 'Книги', 'Другие игры',
                'Консольные игры', 'League of Legends', 'MMO', 'Path of Exile', 'Shooter', 'Battle Royale', 'ККИ, Автобаттлеры', 
                'Hearthstone', 'Artifact', 'Dota Underlords'],
    'Основа' : ['Общие вопросы и обсуждения', 'Обитель нытья', 'Dota Plus, компендиумы и ивенты', 'Обновления и патчи', 
                'Рейтинговая система и статистика', 'Герои: общие обсуждения', 'Dream Dota', 'Нестандартные сборки', 
                'Киберспорт: общие обсуждения', 'Игроки и команды', 'Турниры, матчи и прогнозы', 
                'Поиск игроков для ммр и паб игр', 'Поиск игроков для создания команды', 
                'Поиск команды для совместных игр и участия в турнирах', 'Поиск игроков для ивентов и абузов', 
                'Обмен предметами и гифтами', 'Обсуждения и цены', 'Медиа Dota 2', 'Стримы', 'Развитие портала']
    }
    READY_LIST = [] #Финальный список
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
                        READY_LIST.append(f_link)
    return READY_LIST
