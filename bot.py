import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
import requests
import time
import random
import os
import imglist
import apps
from bs4 import BeautifulSoup as BS
#VARS
processing = False
now = datetime.now()
Bot = commands.Bot(command_prefix='v.')
Bot.remove_command("help")
#Уведомление о кд на команды

#HELP
@Bot.command()
async def help(ctx):
        emb = discord.Embed(title='Виктор', colour=0x33ccff) #Текст выводится с помощью метода Embed
        emb.add_field(name='Информация:', value="\nВерсия: 0.9.9a\n\nВот что я могу:\n\npat @пользователь - погладить юзера <:pat2:672538535156252672>\ncovid - статистика по COVID-19 <:durka:672538535235944488>\nmoder и osnova - <:DankPepe:675661963640045569>")
        await ctx.send(embed = emb)

#PAT
@Bot.command()
async def pat(ctx, member: discord.Member):
    #EMBED метод
    title = str(ctx.author.display_name) + " гладит " + str(member.display_name) + " <:pat2:672538535156252672>" #Название Embed элемента
    emb = discord.Embed(title=title, colour=imglist.CLR_LIST[random.randint(0, imglist.CLR_LIST_LEN)])
    emb.set_image(url=imglist.PAT_LIST[random.randint(0, imglist.PAT_LIST_LEN)])
    await ctx.send(embed = emb)

#covid
@Bot.command()
@commands.cooldown(1, 60, commands.BucketType.guild)
async def covid(ctx):
    covid = apps.covid()
    await ctx.send('Статистика по COVID-19 (З / У / В):\n\nМир: {0} / {1} / {2}\nРоссия: {3} / {4} / {5}\nУкраина: {6} / {7} / {8}\nБеларусь: {9} / {10} / {11}\nРоссия: {12} / {13} / {14}'.format(*covid))

#MODER
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.guild) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def moder(ctx):
    global processing
    if processing == True:
            await ctx.send('Зач используете эту команду во время **osnova**? <:durka:672538535235944488>')
            moder.reset_cooldown(ctx)
    else:
        processing = True
        tick = datetime.now() #TIMER START
        d2ru_category = 'Разное'
        links = apps.d2ru_violations(str(d2ru_category)) #получение списка постов с нарушениями. Функция описана в apps.py
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
        processing = False

@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.guild) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def osnova(ctx):
    global processing
    if processing == True:
        await ctx.send('Зач используете эту команду во время **moder**? <:durka:672538535235944488>')
        osnova.reset_cooldown(ctx)
    else:
        processing = True
        tick = datetime.now() #TIMER START
        d2ru_category = 'Основа'
        links = apps.d2ru_violations(str(d2ru_category)) #получение списка постов с нарушениями. Функция описана в apps.py
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
        processing = False

#END
token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
