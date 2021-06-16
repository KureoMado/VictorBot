#LIBS
import discord
from discord import channel
from discord.ext import commands
from bs4 import BeautifulSoup as BS
from discord.ext.commands import Bot
from datetime import datetime
import time
import random
import os
import config
#Custom
#VARS
now = datetime.now()
Bot = commands.Bot(command_prefix='v.')
Bot.remove_command("help")

@Bot.event
async def on_message(message):
    if message.author.id == 207452566538289162 and message.channel.id != 674776053369012234 and message.channel.id != 672075104632700948 and message.channel.id != 673207142450200616 and message.channel.id != 677159814031212564:
        a = message.content
        if a == 'a' or a == 'b' or a == 'b':
            if a == 'a':
                ch = Bot.get_channel(674776053369012234)
                await ch.send('A B O B A')

            if a == 'b':
                ch = Bot.get_channel(674776053369012234)
                await ch.send('Уважаемые секретари <@!207452566538289162> и <@!649698119671611392>, подсчет актива завершен.')

            if a == 'c':
                ch = Bot.get_channel(674776053369012234)
                await ch.send('Секретари Бобов <@!207452566538289162> и <@!649698119671611392> выражают свое уважение и любовь <@!638380894096195595>! <:pat2:672538535156252672>')
            
            if a == 't':
                ch = Bot.get_channel(677159814031212564)
                await ch.send('Добре <:PuckHmm:672534849776779302>\nУважаемый главарь <@!452518735484289035>. Я - автоматизированный секретарь, провожу контрольные подсчеты актива Бобов. Мои подсчеты точны примерно на 97,5%')
        
        else:
            ch = Bot.get_channel(674776053369012234)
            await ch.send(a)
            


async def aboba(ctx):
    channel = Bot.get_channel(674776053369012234)
    await channel.send('Добре <:PuckHmm:672534849776779302>\nУважаемые секретари <@!207452566538289162> и <@!649698119671611392>, сообщаю что актив бобов будет зачисляться до 15:00. В 17:30 начнется подсчет актива.')

async def tony(ctx):
    channel = Bot.get_channel(677159814031212564)
    await channel.send('Добре <:PuckHmm:672534849776779302>\nУважаемый главарь <@!452518735484289035>. Я - автоматизированный секретарь, провожу контрольные подсчеты актива Бобов. Мои подсчеты точны примерно на 97,5%')

tokenr = config.TOKEN
Bot.run(str(tokenr))
