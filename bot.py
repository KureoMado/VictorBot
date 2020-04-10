import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import time
import random
import os
import imglist
import apps
from datetime import datetime
from bs4 import BeautifulSoup as BS
#V
processing = False
now = datetime.now() #Определение текущей даты
Bot = commands.Bot(command_prefix='m.') #Определение префикса бота
Bot.remove_command("help") #Удаление стандартной хелп-команды

#Консольное уведомление о запуске бота
@Bot.event
async def on_ready():
    print("Mengsk bot is online")
    channel = Bot.get_channel(672075104632700948)
    await channel.send('Менгск тут <:PepeCool:672538535298859038>')

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

#BEGIN

#HELP
@Bot.command()
async def help(ctx):
        emb = discord.Embed(title='Виктор', colour=0x33ccff) #Текст выводится с помощью метода Embed
        emb.add_field(name='Информация:', value="\nВерсия: 0.9.5f\n\nВот что я могу:\n\npat @пользователь - погладить юзера <:pat2:672538535156252672>\nmoder и osnova- сами знаете что <:DankPepe:675661963640045569>")
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
async def covid(ctx, member: discord.Member):
    await ctx.send('placeholder')

#MODER
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.guild) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def moder(ctx):
    global processing
    if processing == True:
            await ctx.send('Зач используете эту команду во время osnova? <:durka:672538535235944488>')
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
        await ctx.send('Зач используете эту команду во время moder? <:durka:672538535235944488>')
        osnova.reset_cooldown(ctx)
    else:
        processing = True
        tick = datetime.now() #TIMER START
        d2ru_category = 'Основа'
        links = apps.d2ru_violations(str(d2ru_category)) #получение списка постов с нарушениями. Функция описана в apps.py
        tock = datetime.now()
        diff = tock - tick
        if len(links) != 0: #Проверка на отсутствие нарушений
            await ctx.send('Результат поиска по **основному** разделу:\nНайдено нарушений: ' + str(len(links)) + '\nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')
            for i in range(len(links)):
                await ctx.send(links[i])
                time.sleep(0.5)
            time.sleep(0.5)
            await ctx.send('На этом все <:MiyanoYey:672534850066055191>')
        else:
            await ctx.send('Результат поиска по **основному** разделу:\nНарушения не найдены <:MiyanoYey:672534850066055191> \nПоиск занял ' + str(int(diff.total_seconds())) + ' сек.')
        processing = False

#END
Bot.run('Njc2ODAzMDAyMzI1MDA4Mzk0.XkLAsg.cV-rKQc6jQjB_5TEgbjkJfZsBzE')
