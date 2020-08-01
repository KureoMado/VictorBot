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
    BAD_WORDS = BAD_WORDS = ['сука', 'сучк*', 'хер', 'херн*', '*хера', '*ахер*', 'похер*',
                             '*хуй*', '*пизд*', 'долбоеб*','*аху*', 'ебат*', 'выеб*',
                             'уеб*', 'съеб*'] #СПИСОК СЛОВ
    CATEGORIES = {
    'Разное' : ['Таверна', 'Творчество', 'Музыка', 'Кино и сериалы', 'Аниме и прочее', 'Спорт', 'Книги', 'Другие игры',
                'Консольные игры', 'League of Legends', 'MMO', 'Path of Exile', 'Shooter, Battle Royale', 'Valorant', 'ККИ, Автобаттлеры',
                'Hearthstone', 'Artifact', 'Dota Underlords'],
    'Основа' : ['Общие вопросы и обсуждения', 'Обитель нытья', 'Dota Plus, компендиумы и ивенты', 'Обновления и патчи',
                'Рейтинговая система и статистика', 'Герои: общие обсуждения', 'Dream Dota', 'Нестандартные сборки',
                'Киберспорт: общие обсуждения', 'Игроки и команды', 'Турниры, матчи и прогнозы',
                'Поиск игроков для ммр и паб игр', 'Поиск игроков для создания команды',
                'Поиск команды для совместных игр и участия в турнирах', 'Поиск игроков для ивентов и абузов',
                'Обмен предметами и гифтами', 'Обсуждения и цены', 'Медиа Dota 2', 'Стримы', 'Развитие портала'],
    'Тех' :    ['Техническая поддержка по Dota 2', 'Железо и обсуждения', 'Сборка ПК, значительный апгрейд',
                'Выбор комплектующих, ноутбуков, консолей', 'Компьютерная помощь по остальным вопросам',
                'Игровые девайсы, периферия и прочая техника', 'Мобильные девайсы', 'Программирование',
                'Steam', 'Софт и прочие технические вопросы']
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

def super_violation():
    #ПОИСК
    BAD_WORDS = BAD_WORDS = ['сука', 'сучк*', 'хер', 'херн*', '*хера', '*ахер*', 'похер*',
                             '*хуй*', '*пизд*', 'долбоеб*','*аху*', 'ебат*', 'выеб*',
                             'уеб*', 'съеб*'] #СПИСОК СЛОВ
    CATEGORIES = {
    'Разное' : ['Таверна', 'Творчество', 'Музыка', 'Кино и сериалы', 'Аниме и прочее', 'Спорт', 'Книги', 'Другие игры',
                'Консольные игры', 'League of Legends', 'MMO', 'Path of Exile', 'Shooter, Battle Royale', 'Valorant', 'ККИ, Автобаттлеры',
                'Hearthstone', 'Artifact', 'Dota Underlords'],
    'Основа' : ['Общие вопросы и обсуждения', 'Обитель нытья', 'Dota Plus, компендиумы и ивенты', 'Обновления и патчи',
                'Рейтинговая система и статистика', 'Герои: общие обсуждения', 'Dream Dota', 'Нестандартные сборки',
                'Киберспорт: общие обсуждения', 'Игроки и команды', 'Турниры, матчи и прогнозы',
                'Поиск игроков для ммр и паб игр', 'Поиск игроков для создания команды',
                'Поиск команды для совместных игр и участия в турнирах', 'Поиск игроков для ивентов и абузов',
                'Обмен предметами и гифтами', 'Обсуждения и цены', 'Медиа Dota 2', 'Стримы', 'Развитие портала'],
    'Тех' :    ['Техническая поддержка по Dota 2', 'Железо и обсуждения', 'Сборка ПК, значительный апгрейд',
                'Выбор комплектующих, ноутбуков, консолей', 'Компьютерная помощь по остальным вопросам',
                'Игровые девайсы, периферия и прочая техника', 'Мобильные девайсы', 'Программирование',
                'Steam', 'Софт и прочие технические вопросы']
    }
    RAW_LIST = [] #список без исключений
    tavern_list = []
    osnova_list = []
    tech_list = []
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
                    #оформление сообщения
                    div = div_search[dsc]
                    f_link = 'Возможное нарушение: **' + str(BAD_WORDS[i]) + '**\nhttps://dota2.ru/forum/' + str(div.select('a')[0]['href'])
                    if str(get_cat[1].text) in CATEGORIES['Разное']:
                        tavern_list.append(f_link)
                    if str(get_cat[1].text) in CATEGORIES['Основа']:
                        osnova_list.append(f_link)
                    if str(get_cat[1].text) in CATEGORIES['Тех']:
                        tech_list.append(f_link)
        #Проверка на исключения
    tavern_list = post_exc(tavern_list)
    osnova_list = post_exc(osnova_list)
    tech_list = post_exc(tech_list)
    return (tavern_list, osnova_list, tech_list)
