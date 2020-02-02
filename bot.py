import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import time
import random
import imglist
import os
from bs4 import BeautifulSoup as BS

#BOTS COMMANDS

Bot = commands.Bot(command_prefix='v.')

#Turn On notification
@Bot.event
async def on_ready():
    print("Neko bot is online")

#PuckHmm reaction
@Bot.event
async def on_message(ctx):
    channel = ctx.channel
    isbot = ctx.author.bot
    if isbot == False:
        if ctx.content == "<:PuckHmm:672534849776779302>":
            await channel.send("<:PuckHmm:672534849776779302>")
    await Bot.process_commands(ctx)

#test
@Bot.command(pass_context = True)
async def test(ctx):
    await ctx.send("test")
    #await ctx.send("{}".format(ctx.message.author.mention))

#avatar
@Bot.command(pass_context = True)
async def av(ctx):
    usrid = random.randint(100000,700000)
    #usrpg = 'https://dota2.ru/forum/members/' + str(usrid)
    usrpg = 'https://dota2.ru/forum/members/' + str(usrid)

    r = requests.get(usrpg)
    html = BS(r.content, 'html.parser')

    av = html.select('.avatar > img.my')[0]['src']
    av_url = "https://dota2.ru" + str(av)
    await ctx.send(av_url)
    await ctx.send(usrpg)


#Embed IMG
@Bot.command(pass_context = True)
async def img(ctx):
    testm = "check"
    emb = discord.Embed(title="testm", colour=0x39d0d6)
    emb.set_image(url="https://dota2.ru/img/forum/avatars/l/638/638867.jpg")
    await ctx.send(embed = emb)


#VICTOR
@Bot.command()
async def pat(ctx, member: discord.Member):
    #RANDOM GIF AND COLOR
    pat_number = random.randint(0, imglist.PAT_LIST_LEN)
    color_number = random.randint(0, imglist.CLR_LIST_LEN)
    #GIF AND COLOR SET
    pat = imglist.PAT_LIST[pat_number]
    color = imglist.CLR_LIST[color_number]
    #EMBED
    author = str(ctx.author.name)
    nick = str(member.nick)
    title = author + " pats " + nick
    emb = discord.Embed(title=title, colour=color)
    emb.set_image(url=pat)
    await ctx.send(embed = emb)

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
