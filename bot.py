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

@Bot.event
async def on_command_error(self, error):
    channel = self.channel
    if isinstance(error, commands.CommandOnCooldown):
        await channel.send('Эта команда была использована сосвем недавно! Вам придется подождать еше %.2f секунд <:MiyanoYey:672534850066055191>' % error.retry_after)
    raise error

#PuckHmm reaction
@Bot.event
async def on_message(ctx):
    channel = ctx.channel
    isbot = ctx.author.bot
    if isbot == False:
        if "<:PuckHmm:672534849776779302>" in ctx.content:
            await ctx.add_reaction("<:PuckHmm:672534849776779302>")
    await Bot.process_commands(ctx)

#test
@Bot.command()
async def help(ctx):
        emb = discord.Embed(title='Виктор', colour=0x33ccff)
        emb.add_field(name='Информация:', value="\nВерсия: 0.9.2\n\nВот что я могу:\n\npat @пользователь - погладить юзера\nvictor - арт с Виктором\nТакже я фанат смайла <:PuckHmm:672534849776779302> и буду ставить его под все сообщения где он есть!")
        await ctx.send(embed = emb)

#PAT
@Bot.command()
async def pat(ctx, member: discord.Member):
    #RANDOM GIF AND COLOR
    pat_number = random.randint(0, imglist.PAT_LIST_LEN)
    color_number = random.randint(0, imglist.CLR_LIST_LEN)
    #GIF AND COLOR SET
    pat = imglist.PAT_LIST[pat_number]
    color = imglist.CLR_LIST[color_number]
    #EMBED
    author = str(ctx.author.display_name)
    nick = str(member.display_name)
    title = author + " гладит " + nick + " :3"
    emb = discord.Embed(title=title, colour=color)
    emb.set_image(url=pat)
    await ctx.send(embed = emb)

#VICTOR
@Bot.command()
async def victor(ctx):
    #RANDOM GIF AND COLOR
    v_number = random.randint(0, imglist.VICTOR_LIST_LEN)
    clr_number = random.randint(0, imglist.CLR_LIST_LEN)
    #GIF AND COLOR SET
    victor = imglist.VICTOR_LIST[v_number]
    color = imglist.CLR_LIST[clr_number]
    #EMBED
    emb = discord.Embed(title=' ', colour=color)
    emb.set_image(url=victor)
    await ctx.send(embed = emb)

#RANDOM THREAD
@Bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def vbros(ctx):
    href = rntv.random_thread()
    ctxout = "Рандомный вброс с первой страницы таверны:\n" + str(href)
    await ctx.send(ctxout)

#VIDEO
@Bot.command()
async def video(ctx):
    await ctx.send('https://www.youtube.com/watch?v=oqR2YnmXSAY')

#BAD WORDS SEARCH FOR MODERS
@Bot.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
@commands.has_permissions(administrator = True)
async def moder(ctx):
    links = rntv.mat_search()
    if len(links) != 0:
        await ctx.send('Мне кажется, в этих сообщениях (всего ' + str(len(links)) + ') есть нарушения:')
        for i in range(len(links)):
            await ctx.send(links[i])
            time.sleep(1)
        time.sleep(2)
        await ctx.send('{.author.mention}, пожалуйста, помогите мне улучшить бота! Если в сообщении действительно было нарушение - поставьте в реакции смайл <:MiyanoYey:672534850066055191>. Если нарушения не было ставьте - <:PuckHmm:672534849776779302>. Если сообщениию больше 3 дней - <:GWnonMuugu:672538535341064252>. Если сообщение не из наших разделов - <:MiyanoWhat:672538535395590174>. Спасибо!'.format(ctx))
    else:
        await ctx.send('Похоже, нарушений нет <:MiyanoYey:672534850066055191>')


token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
