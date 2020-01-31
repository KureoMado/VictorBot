import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import time
import random
import os
from bs4 import BeautifulSoup as BS

#PARSER

#avi = av.select('img')
#ava = avi[0]['src']

#BOTS COMMANDS

Bot = commands.Bot(command_prefix='v!')

@Bot.event
async def on_message(ctx):
    channel = ctx.channel
    isbot = ctx.author.bot
    if isbot == False:
        if ctx.content == "<:PuckHmm:672534849776779302>":
            await Bot.send_message(channel, "<:PuckHmm:672534849776779302>")
    await Bot.process_commands(ctx)

@Bot.command(pass_context = True)
async def test(ctx):
    await Bot.say("Test passed")

@Bot.command(pass_context = True)
async def av(ctx):
    usrid = random.randint(100000,700000)
    #usrpg = 'https://dota2.ru/forum/members/' + str(usrid)
    usrpg = 'https://dota2.ru/forum/members/' + str(usrid)

    r = requests.get(usrpg)
    html = BS(r.content, 'html.parser')

    av = html.select('.avatar > img.my')[0]['src']
    av_url = "https://dota2.ru" + str(av)
    await Bot.say(av_url)
    await Bot.say(usrpg)


#Embed IMG
@Bot.command(pass_context = True)
async def img(ctx):
    testm = "check"
    emb = discord.Embed(title="testm", colour=0x39d0d6)
    emb.set_image(url="https://dota2.ru/img/forum/avatars/l/638/638867.jpg")
    await Bot.say(embed = emb)


token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
