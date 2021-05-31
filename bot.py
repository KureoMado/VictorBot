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

async def my_background_task():
    await Bot.wait_until_ready()
    while True:
        a = ''
        input(a)
        if a == 1:
            ch = Bot.get_channel(674776053369012234)
            await ch.send('Добре <:PuckHmm:672534849776779302>\nУважаемые секретари <@!207452566538289162> и <@!649698119671611392>, сообщаю что актив бобов будет зачисляться до 15:00. В 17:30 начнется подсчет актива.')

        if a == 2:
            ch = Bot.get_channel(674776053369012234)
            await ch.send('Уважаемые секретари <@!207452566538289162> и <@!649698119671611392>, подсчет актива начинается. Результаты будут готовы 01.06.2021')

        if a == 3:
            ch = Bot.get_channel(674776053369012234)
            await ch.send('Секретари Бобов <@!207452566538289162> и <@!649698119671611392> выражают свое уважение и любовь <@!638380894096195595>! <:pat2:672538535156252672>')



async def aboba(ctx):
    channel = Bot.get_channel(674776053369012234)
    await channel.send('Добре <:PuckHmm:672534849776779302>\nУважаемые секретари <@!207452566538289162> и <@!649698119671611392>, сообщаю что актив бобов будет зачисляться до 15:00. В 17:30 начнется подсчет актива.')


#END
Bot.loop.create_task(my_background_task())
tokenr = config.TOKEN
Bot.run(str(tokenr))
