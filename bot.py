import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import time
import random
import os
from bs4 import BeautifulSoup as BS
#BOTS COMMANDS

Bot = commands.Bot(command_prefix='v!')

#Turn On notification
@Bot.event
async def on_ready():
    print("Neko bot is online")

#Testment
@Bot.command(pass_context = True)
async def test(ctx):
    await ctx.send("Test passed")

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
   
@Bot.command(pass_context = True)
async def cmds(ctx):
    await ctx.send("Тут есть: test, img, av")

Bot.run('NjcyMDM1ODQwNDI3Mjk0NzI0.XjFoNw.dyXrx-ZKzgC47v99Lqk0STIX9Yg')
