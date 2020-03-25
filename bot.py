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
Bot = commands.Bot(command_prefix='v.')
now = datetime.now()
excpts = []
Bot.remove_command("help")
#Уведомление о кд на команды

#приветствие
@Bot.event
async def on_ready():
    channel = Bot.get_channel(674776053369012234)
    await channel.send('Бот запущен! <:MiyanoYey:672534850066055191>\nТекущая версия - 0.9.6b\n\nИзменения:\n-Добавлена команда osnova\n-Поиск ускорен на 1 секунду\n-Добавление в исключения временно отключено')

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

#HELP
@Bot.command()
async def help(ctx):
        emb = discord.Embed(title='Виктор', colour=0x33ccff) #Текст выводится с помощью метода Embed
        emb.add_field(name='Информация:', value="\nВерсия: 0.9.5f\n\nВот что я могу:\n\npat @пользователь - погладить юзера <:pat2:672538535156252672>\nmoder - сами знаете что <:DankPepe:675661963640045569>")
        await ctx.send(embed = emb)

#PAT
@Bot.command()
async def pat(ctx, member: discord.Member):
    #EMBED метод
    title = str(ctx.author.display_name) + " гладит " + str(member.display_name) + " <:pat2:672538535156252672>" #Название Embed элемента
    emb = discord.Embed(title=title, colour=imglist.CLR_LIST[random.randint(0, imglist.CLR_LIST_LEN)])
    emb.set_image(url=imglist.PAT_LIST[random.randint(0, imglist.PAT_LIST_LEN)])
    await ctx.send(embed = emb)

#MODER
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.guild) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def moder(ctx):
    global excpts
    d2ru_category == 'Разное'
    links = apps.d2ru_violations(str(d2ru_category)) #получение списка постов с нарушениями. Функция описана в apps.py
    if len(links) != 0: #Проверка на отсутствие нарушений
        if excpts != 0:
            try:
                links = list(set(links) - set(excpts))
            except:
                pass
        await ctx.send('В разделе **РАЗНОЕ** найдено (всего ' + str(len(links)) + ') нарушений:')
        for i in range(len(links)):
            await ctx.send(links[i])
            time.sleep(0.5)
        time.sleep(0.5)
        await ctx.send('На этом все <:MiyanoYey:672534850066055191>\nДобавить в исключения - <:ShrekOMG:672538535483670549>')
    else:
        await ctx.send('Я ничего не нашел <:pat:672538535164772392>')

@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.guild) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def osnova(ctx):
    global excpts
    d2ru_category == 'Основа'
    links = apps.d2ru_violations(str(d2ru_category)) #получение списка постов с нарушениями. Функция описана в apps.py
    if len(links) != 0: #Проверка на отсутствие нарушений
        if excpts != 0:
            try:
                links = list(set(links) - set(excpts))
            except:
                pass
        await ctx.send('В разделе **ОСНОВА** найдено (всего ' + str(len(links)) + ') нарушений:')
        for i in range(len(links)):
            await ctx.send(links[i])
            time.sleep(0.5)
        time.sleep(0.5)
        await ctx.send('На этом все <:MiyanoYey:672534850066055191>')
    else:
        await ctx.send('Я ничего не нашел <:pat:672538535164772392>')

#BOT START
token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
