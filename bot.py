#LIBS
import discord
from discord import channel
from discord.ext import commands
from bs4 import BeautifulSoup as BS
from discord.ext.commands import Bot
from datetime import datetime
import psycopg2
import requests
import time
import random
import os
#Custom
import config
import imglist
import apps
#VARS
now = datetime.now()
Bot = commands.Bot(command_prefix=config.PREFIX)
Bot.remove_command("help")

#Консольное уведомление о запуске бота
@Bot.event
async def on_ready():
    channel = Bot.get_channel(739121375016386682)
    await channel.send('Пий XIII был запущен')

@Bot.event
async def on_command_error(self, error):
    channel = self.channel
    if isinstance(error, commands.CommandOnCooldown):
        awt = int(error.retry_after)
        if awt >= 60:
            awt_m =  awt // 60
            await channel.send('Эта команда была использована сосвем недавно! Вам придется подождать еще %i мин. <:HZ:672538535781335045>' % awt_m)
        else:
            await channel.send('Эта команда была использована сосвем недавно! Вам придется подождать еще %i сек. <:HZ:672538535781335045>' % error.retry_after)
    if isinstance(error, commands.CommandNotFound):
            await channel.send('Не понимаю о чем вы <:PuckHmm:672534849776779302>')

@Bot.event
async def on_raw_reaction_add(ctx):
    global excpts
    channel = Bot.get_channel(ctx.channel_id)
    msgr = await channel.fetch_message(ctx.message_id)
    st = msgr.content.startswith('Возможное нарушение:')
    if st == True and msgr.author.bot == True and str(ctx.emoji) == '<:ShrekOMG:672538535483670549>':
        apps.db_write(str(msgr.content[-9:-1]));
        to_send = 'Пост #' + str(msgr.content[-9:-1]) + ' добавлен в исключения! <:MiyanoYey:672534850066055191>'
        await channel.send(to_send)

#HELP
@Bot.command()
async def help(ctx):
        emb = discord.Embed(title='Пий XIII', colour=0x33ccff) #Текст выводится с помощью метода Embed
        emb.add_field(name='Информация:', value="\nВерсия: 0.9.9c\n\nВот что я могу:\n\npat @пользователь - погладить юзера <:pat2:672538535156252672>\ncovid - статистика по COVID-19 <:durka:672538535235944488>\nmoder и osnova - <:DankPepe:675661963640045569>")
        await ctx.send(embed = emb)

#MODER
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def moder(ctx):
    tick = datetime.now() #TIMER START
    links = apps.d2ru_violations('Разное') #получение списка постов с нарушениями. Функция описана в apps.py
    tock = datetime.now()
    diff = tock - tick
    if len(links) != 0: #Проверка на отсутствие нарушений
        await ctx.send('Результат поиска в **других играх и разном**:\nНайдено нарушений: ' + str(len(links)) + '\nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')
        for i in range(len(links)):
            await ctx.send(links[i])
            time.sleep(0.5)
        time.sleep(0.5)
        await ctx.send('На этом все <:MiyanoYey:672534850066055191>')
    else:
        await ctx.send('Результат поиска в **других играх и разном**:\nНарушения не найдены <:MiyanoYey:672534850066055191> \nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')

@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def osnova(ctx):
    tick = datetime.now() #TIMER START
    links = apps.d2ru_violations('Основа') #получение списка постов с нарушениями. Функция описана в apps.py
    tock = datetime.now()
    diff = tock - tick
    if len(links) != 0: #Проверка на отсутствие нарушений
        await ctx.send('Результаты поиска по **основному** разделу:\n\nНайдено нарушений: ' + str(len(links)) + '\n\nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')
        for i in range(len(links)):
            await ctx.send(links[i])
            time.sleep(0.5)
        time.sleep(0.5)
        await ctx.send('На этом все <:MiyanoYey:672534850066055191>')
    else:
        await ctx.send('Результат поиска по **основному** разделу:\nНарушения не найдены <:MiyanoYey:672534850066055191> \nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')

#поиск в техе
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def tech(ctx):
    tick = datetime.now() #TIMER START
    links = apps.d2ru_violations('Тех') #получение списка постов с нарушениями. Функция описана в apps.py
    tock = datetime.now()
    diff = tock - tick
    if len(links) != 0: #Проверка на отсутствие нарушений
        await ctx.send('Результат поиска в **техническом разделе**:\nНайдено нарушений: ' + str(len(links)) + '\nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')
        for i in range(len(links)):
            await ctx.send(links[i])
            time.sleep(0.5)
        time.sleep(0.5)
        await ctx.send('На этом все <:MiyanoYey:672534850066055191>')
    else:
        await ctx.send('Результат поиска в **техническом разделе**:\nНарушения не найдены <:MiyanoYey:672534850066055191> \nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')

#super
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def super(ctx):
    tick = datetime.now() #TIMER START
    links =  apps.super_violation() #получение списка постов с нарушениями. Функция описана в apps.py
    tock = datetime.now()
    diff = tock - tick
    if len(links[0]) != 0: #Проверка на отсутствие нарушений
        await ctx.send('Результат поиска в **других играх и разном**:\nНайдено нарушений: ' + str(len(links[0])))
        for i in range(len(links[0])):
            await ctx.send(links[0][i])
            time.sleep(0.5)
        time.sleep(1)
    else:
        await ctx.send('В **других играх и разном** ничего не найдено <:ChildPepeCry:672538534493814825>')
        time.sleep(1)

    await ctx.send('<:Addsky:672537907680247828><:Addsky:672537907680247828><:Addsky:672537907680247828> ')

    if len(links[1]) != 0: #Проверка на отсутствие нарушений
        await ctx.send('Результат поиска в **основном разделе**:\nНайдено нарушений: ' + str(len(links[1])))
        for i in range(len(links[1])):
            await ctx.send(links[1][i])
            time.sleep(0.5)
        time.sleep(1)
    else:
        await ctx.send('В **оснонвом разделе** ничего не найдено <:ChildPepeCry:672538534493814825>')
        time.sleep(1)

    await ctx.send('<:Addsky:672537907680247828><:Addsky:672537907680247828><:Addsky:672537907680247828> ')

    if len(links[2]) != 0: #Проверка на отсутствие нарушений
        await ctx.send('Результат поиска в **техническом**:\nНайдено нарушений: ' + str(len(links[2])))
        for i in range(len(links[2])):
            await ctx.send(links[2][i])
            time.sleep(0.5)
        time.sleep(1)
    else:
        await ctx.send('В **техническом** ничего не найдено <:ChildPepeCry:672538534493814825>')
        time.sleep(1)
    await ctx.send('На этом все <:MiyanoYey:672534850066055191>\nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')

#END
tokenr = config.TOKEN
Bot.run(str(tokenr))
