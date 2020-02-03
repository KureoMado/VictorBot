import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import time
import random
import imglist
import rntv
import tavern
from bs4 import BeautifulSoup as BS

#BOTS COMMANDS

Bot = commands.Bot(command_prefix='v.')
Bot.remove_command("help")

#Turn On notification
@Bot.event
async def on_ready():
    print("Neko bot is online")

@Bot.command()
async def newthreadstart(ctx):
    svd = 'none'
    while True:
        src = tavern.tavern_thread()
        if src != svd and src != None:
            await ctx.send(src)
            svd = src
        time.sleep(30)
    await ctx.send('empty')

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
        emb.add_field(name='Версия: 0.7.4', value="\nВот что я могу:\n\npat @пользователь - погладить юзера\nvictor - арт с Виктором\nТакже я фанат смайла <:PuckHmm:672534849776779302> и буду ставить его под все сообщения где он есть!")
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
async def vbros(ctx):
    href = rntv.random_thread()
    ctxout = "Рандомный вброс с первой страницы таверны:\n" + str(href)
    await ctx.send(ctxout)

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
