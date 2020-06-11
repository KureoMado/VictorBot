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
processing = False
now = datetime.now()
Bot = commands.Bot(command_prefix=config.PREFIX)
Bot.remove_command("help")

"""
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
            await channel.send('Не понимаю о чем вы <:PuckHmm:672534849776779302>') """

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
    await ctx.send('Статистика по COVID-19 (З / У / В):\n\nМир: {0} / {1} / {2}\nРоссия: {3} / {4} / {5}\nУкраина: {6} / {7} / {8}\nБеларусь: {9} / {10} / {11}\nКазахстан: {12} / {13} / {14}'.format(*covid))

#MODER
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def moder(ctx):
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

@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def osnova(ctx):
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

#END
tokenr = config.TOKEN
Bot.run(str(tokenr))
