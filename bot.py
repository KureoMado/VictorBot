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
@Bot.command()
async def version(ctx):
        emb = discord.Embed(title='Виктор', colour=0x33ccff)
        emb.add_field(name='Информация', value="\nВот что я могу:\npat @пользователь - погладить юзера\n\nvictor - арт с Виктором\n\nТакже я фанат смайла <:PuckHmm:672534849776779302> и буду отвечать на него!")
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
    nick = str(member.nick)
    title = author + " pats " + nick
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

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
