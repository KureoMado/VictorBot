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
import rntv
from bs4 import BeautifulSoup as BS

#BOTS COMMANDS

Bot = commands.Bot(command_prefix='v.')
Bot.remove_command("help")
now = datetime.now()
excpts = []

#Уведомление о кд на команды
@Bot.event
async def on_command_error(self, error):
    channel = self.channel
    if isinstance(error, commands.CommandOnCooldown):
        awt = int(error.retry_after)
        if awt >= 60:
            awt_m =  awt // 60
            await channel.send('Эта команда была использована сосвем недавно! Вам придется подождать еще %i мин. <:MiyanoYey:672534850066055191>' % awt_m)
        else:
            await channel.send('Эта команда была использована сосвем недавно! Вам придется подождать еще %i сек. <:MiyanoYey:672534850066055191>' % error.retry_after)

@Bot.event
async def on_raw_reaction_add(ctx):
    global excpts
    cid = ctx.channel_id
    emoj = ctx.emoji
    channel = Bot.get_channel(cid)
    msgr = await channel.fetch_message(ctx.message_id)
    msg = msgr.content
    botchk = msgr.author.bot
    st = msg.startswith('Возможное нарушение:')
    if msg[-9:-1] in excpts:
        pass
    else:
        if st == True and botchk == True and str(emoj) == '<:ShrekOMG:672538535483670549>':
            excpts.append(msg)
            to_send = 'Пост #' + str(msg[-9:-2]) + ' добавлен в исключения! <:MiyanoYey:672534850066055191>'
            await channel.send(to_send)


#HELP
@Bot.command()
async def help(ctx):
        emb = discord.Embed(title='Виктор', colour=0x33ccff) #Текст выводится с помощью метода Embed
        emb.add_field(name='Информация:', value="\nВерсия: 0.9.4a\n\nВот что я могу:\n\npat @пользователь - погладить юзера\nvictor - арт с Виктором\nmoder - поиск нарушений на д2ру. Кд - 30 минут\nvbros - рандомный вброс с 1 страницы товерны\n\nТакже я фанат смайла <:PuckHmm:672534849776779302> и буду ставить его под все сообщения где он есть!")
        await ctx.send(embed = emb)

#PAT
@Bot.command()
async def pat(ctx, member: discord.Member):
    #Определение гифки и цвета полоски слева. Берется рандомный элемент списка из imglist
    pat = imglist.PAT_LIST[random.randint(0, imglist.PAT_LIST_LEN)]
    color = imglist.CLR_LIST[random.randint(0, imglist.CLR_LIST_LEN)]
    #EMBED метод
    author = str(ctx.author.display_name) #Определение имени отправителя
    nick = str(member.display_name) # Опделеление имени отправителя
    title = author + " гладит " + nick + " :3" #Название Embed элемента
    emb = discord.Embed(title=title, colour=color)
    emb.set_image(url=pat)
    await ctx.send(embed = emb)

#VICTOR
@Bot.command()
async def victor(ctx):
    #Определение пикчи и цвета полоски слева. Берется рандомный элемент списка из imglist
    victor = imglist.VICTOR_LIST[random.randint(0, imglist.VICTOR_LIST_LEN)]
    color = imglist.CLR_LIST[random.randint(0, imglist.CLR_LIST_LEN)]
    #EMBED
    emb = discord.Embed(title=' ', colour=color)
    emb.set_image(url=victor)
    await ctx.send(embed = emb)

#RANDOM THREAD
@Bot.command()
async def vbros(ctx):
    #Функция random_thread() находится в rntv.py
    href = rntv.random_thread()
    ctxout = "Рандомный вброс с первой страницы таверны:\n" + str(href)
    await ctx.send(ctxout)

#Временная команда для теста видоса
@Bot.command()
@commands.cooldown(1, 10, commands.BucketType.guild)
async def video(ctx):
    video = ['https://youtu.be/RoJsKV6-e9M', 'https://www.youtube.com/watch?v=oqR2YnmXSAY']
    await ctx.send(video[random.randint(0,1)])

#Поиск нарушений и выдача их
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.guild) #Кд в 30 минут
@commands.has_permissions(administrator = True) #Команду могут использовать только администраторы сервера
async def moder(ctx):
    global excpts
    links = rntv.mat_search() #получение списка постов с нарушениями. Функция описана в rntv.py
    if len(links) != 0: #Проверка на отсутствие нарушений
        if excpts != 0:
            try:
                links = list(set(links) - set(excpts))
            except:
                pass
        await ctx.send('Мне кажется, в этих сообщениях (всего ' + str(len(links)) + ') есть нарушения:')
        for i in range(len(links)):
            await ctx.send(links[i])
            time.sleep(1)
        time.sleep(1)
        await ctx.send('{.author.mention}, поставьте результатам реацию: Виктор правильно выявил нарушение - <:MiyanoYey:672534850066055191>. Ошибся - <:PuckHmm:672534849776779302>. Если хотите добавить сообщение в исключения - <:ShrekOMG:672538535483670549>'.format(ctx))
    else:
        await ctx.send('Похоже, нарушений нет <:MiyanoYey:672534850066055191>')

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
