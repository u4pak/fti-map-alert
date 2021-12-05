import requests

import pathlib

import json

import time

import discord
from discord.ext import commands
TOKEN = "Put Your Bot Token Here" # https://discord.com/developers/

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

mapData = requests.get('https://fliptheisland.com/data.json')

devMode = 0

timeVar = time.localtime()
current_time = time.strftime("%H:%M:%S", timeVar)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='https://fliptheisland.com/'))

    pathlib.Path('mapdata.json').write_bytes(mapData.content)
    with open('mapdata.json') as f:
        data = json.load(f)

    currentMapUrl = data['mapUrl']

    devMapUrl = 'fakeDataForDevMode'

    while True:
        pathlib.Path('mapdata.json').write_bytes(mapData.content)
        with open('mapdata.json') as f:
            data = json.load(f)

        if devMode >= 1:
            if data['mapUrl'] == devMapUrl:
                print('The map is the same.')
            else:
                print('The map is different! Sending message to channel...')
                channel = bot.get_channel('PUT YOUR CHANNEL ID HERE') # PUT IT AS AN INTEGER, NOT A STRING

                await channel.send('@everyone')

                embed = discord.Embed(
                    title = 'NEW MAP JUST DROPPED',
                    description = 'Image URL: https://fliptheisland.com' + data['mapUrl'],
                    colour = discord.Colour.blue()
                )

                embed.set_image(url='https://fliptheisland.com' + data['mapUrl'])
                embed.set_footer(text='Revealed at ' + str(current_time) + ' PST | ' + str(data['progress']) + '%')

                devMapUrl = data['mapUrl']

                await channel.send(embed=embed)

        else:
            if data['mapUrl'] == currentMapUrl:
                print('The map is the same.')
            else:
                print('The map is different! Sending message to channel...')
                channel = bot.get_channel('PUT YOUR CHANNEL ID HERE') # PUT IT AS AN INTEGER, NOT A STRING

                await channel.send('@everyone')

                embed = discord.Embed(
                    title = 'NEW MAP JUST DROPPED',
                    description = 'Image URL: https://fliptheisland.com' + data['mapUrl'],
                    colour = discord.Colour.blue()
                )

                embed.set_image(url='https://fliptheisland.com' + data['mapUrl'])
                embed.set_footer(text='Revealed at ' + str(current_time) + ' PST | ' + str(data['progress']) + '%')

                currentMapUrl = data['mapUrl']

                await channel.send(embed=embed)
        
        time.sleep(5)
        

bot.run(TOKEN)
